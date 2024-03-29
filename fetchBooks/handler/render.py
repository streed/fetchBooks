import boto
import datetime
import os
import re
import tempfile
import time

from boto.s3.key import Key

from collections import defaultdict

from jinja2 import Environment, FileSystemLoader

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from weasyprint import HTML, CSS

from ..fetch.fetchBooks.FetchBooksService import Iface, Processor, Client
from ..fetch.fetchBooks.ttypes import FetchBooksResponse, Invoice, Order, Restaurant, Item


class FetchBooks( Iface ):

    env = None

    def __init__( self ):
        if( not FetchBooks.env ):
            FetchBooks.env = Environment( loader=FileSystemLoader( os.path.join( os.path.dirname( __file__ ), "..", "templates" ) ) )

    @classmethod
    def makeServer( cls, port=30303 ):
        handler = cls()
        processor = Processor( handler )
        transport = TSocket.TServerSocket( port=port )
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        server = TServer.TSimpleServer( processor, transport, tfactory, pfactory )

        return server

    @classmethod
    def makeClient( cls, address='localhost', port=30303 ):
        transport = TSocket.TSocket( address, port )
        transport = TTransport.TBufferedTransport( transport )
        protocol = TBinaryProtocol.TBinaryProtocol( transport )
        client = Client( protocol )

        transport.open()

        return client

    @classmethod
    def invoiceFromJson( cls, invoice ):
        def foodFromJson( f ):
            i = f["item"]
            item = Item()
            
            item.name = i["name"]
            item.qty = int( i["qty"] )
            item.subtotal = float( i["line_subtotal"] )
            item.total = float( i["line_total"] )
            item.tax = float( i["line_tax"] )

            return item

        i = Invoice()
        i.restaurants = []

        foods = invoice["food"]

        rs = defaultdict( list )

        for f in foods:
            if f.item.name != "Tips":
                rs[f["restaurant"]].append( foodFromJson( f ) )

        for k in rs:
            restaurant = Restaurant()
            order = Order()
            order.id = invoice["order"]["id"]
            order.order_date = invoice["order"]["order_date"]
            order.tax = 0.0
            order.subtotal = 0.0
            order.food = rs[k]
            for f in order.food:
                order.tax += f.tax
                order.subtotal += f.total
            order.total = order.tax + order.subtotal
            restaurant.order = order
            restaurant.name = k
            i.restaurants.append( restaurant )

        return i


    def render_invoice( self, invoice ):
        conn = boto.connect_s3()
        bucket = conn.get_bucket( "fetchbooks" )

        response = FetchBooksResponse()
        response.timestamp = int( time.time() )
        response.invoiceUrl = ""

        template = FetchBooks.env.get_template( "invoice.html" )

        for r in invoice.restaurants:

            html = template.render( restaurant=r )

            f, path = tempfile.mkstemp()

            path2 = "/home/elchupa/code/fetch/fetchBooks/fetchBooks/static/%s.pdf" % r.order.id

            HTML( string=html ).write_pdf( path, stylesheets=[CSS( string=FetchBooks.env.get_template( "invoice.css" ).render() )] )

            HTML( string=html ).write_pdf( path2, stylesheets=[CSS( string=FetchBooks.env.get_template( "invoice.css" ).render() )] )

            k = Key( bucket )
            key = "invoices/%s/%s/%s.pdf" % ( r.name, datetime.date.today(), r.order.id )
            k.key = key
            k.set_contents_from_filename( path )

            response.invoiceUrl = key
        
        return  response

