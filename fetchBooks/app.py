import boto
import json
import glob
from flask import Flask, request, render_template
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

path_template = "/home/elchupa/code/fetch/fetchBooks/fetchBooks/static/%s"


@app.route( "/" )
def index():
  pdfs = glob.glob( path_template % "*.pdf" ) 

  print pdfs

  return render_template( "simple.html", pdfs=pdfs )


@app.route( "/pdfs/<pdf>" )
def pdf_link( pdf ):
    p = path_template % ( "%s.pdf" % pdf )
    print p
    return app.send_static_file( p )
