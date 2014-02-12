import time

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from ..fetch.fetchBooks.FetchBooksService import Iface, Processor, Client
from ..fetch.fetchBooks.ttypes import FetchBooksResponse, Invoice, Order, Food


class FetchBooks( Iface ):

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
        i = Invoice()
        o = Order()

        i.invoiceNumber = invoice["invoiceNumber"]
        i.invoiceDate = invoice["invoiceDate"]
        i.restaurant_name = invoice["restaurant_name"]
        i.restaurant_address = invoice["restaurant_address"]
        i.restaurant_contact = invoice["restaurant_contact"]

        order = invoice["order"]

        o.subTotal = order["subTotal"]
        o.tax = order["tax"]
        o.discountPercentage = order["discountPercentage"]
        o.food = []

        foods = order["food"]

        for f in foods:
            ff = Food()
            ff.item = f["item"]
            ff.description = f["description"]
            ff.quantity = f["quantity"]
            ff.unitCost = f["unitCost"]

            o.food.append( ff )

        i.order = o

        return i


    def render_invoice( self, invoice ):
        print invoice
        print invoice.order
        print invoice.order.foods

        response = FetchBooksResponse()
        response.timestamp = int( time.time() )
        response.invoiceUrl = "http://test.com"

        return  response

    def get_update( self, currentStatus ):
        print "Got a update request."

        return None


