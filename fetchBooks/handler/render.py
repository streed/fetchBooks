import boto
import os
import time

from collections import defaultdict

from jinja2 import Environment, FileSystemLoader

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from weasyprint import HTML

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

            return item

        i = Invoice()
        i.restaurants = []

        foods = invoice["food"]

        rs = defaultdict( list )

        for f in foods:
            rs[f["restaurant"]].append( foodFromJson( f ) )

        for k in rs:
            restaurant = Restaurant()
            order = Order()
            order.id = invoice["order"]["id"]
            order.total = float( invoice["order"]["order_total"] )
            order.order_date = invoice["order"]["order_date"]
            order.food = rs[k]
            restaurant.order = order
            restaurant.name = k
            i.restaurants.append( restaurant )

        return i


    def render_invoice( self, invoice ):

        response = FetchBooksResponse()
        response.timestamp = int( time.time() )
        response.invoiceUrl = "http://test.com"

        template = FetchBooks.env.get_template( "invoice.html" )

        for r in invoice.restaurants:

            html = template.render( restaurant=r )

            print HTML( string=html ).write_pdf( "/tmp/test.pdf" )

        
        return  response

