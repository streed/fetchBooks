import json
from flask import Flask, request
from flask.ext.restful import Api, Resource

from .handler.render import FetchBooks as FB

app = Flask( __name__ )
api = Api( app )

class FetchBooks( Resource ):

    def post( self ):
        invoice = request.json

        invoice = FB.invoiceFromJson( invoice )

        client = FB.makeClient()

        ret = client.render_invoice( invoice )

        print ret

        return { "status": ret.status, "timestamp": ret.timestamp, "invoiceUrl": ret.invoiceUrl }

api.add_resource( FetchBooks, "/invoice" )





