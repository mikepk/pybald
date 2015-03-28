from optparse import OptionParser
from wsgiref.simple_server import make_server
from pybald.util.static_serve import StaticServer
import sys
import os

def serve(app):
    parser = OptionParser()
    parser.add_option("--host", default="0.0.0.0",
                      dest="host",
                      help="host ip to run")
    parser.add_option("-p", "--port",
                      type="int",
                      dest="port", default=8080,
                      help="the port to run on.")
    (options, args) = parser.parse_args()

    # add the static server component
    my_app = StaticServer(app, path=os.path.join('.', 'public'))
    httpd = make_server(options.host, options.port, my_app)
    print("Serving on {0}:{1}...".format(options.host, options.port))
    httpd.serve_forever()