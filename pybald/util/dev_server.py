import sys
from sys import stdout


def start_dev_server(app, options=None):
    '''Create a development web WSGI server using the standard library
    wsgiref module and serve the pybald application.

    This is not intended for production use.

    :param app: wsgi application passed in
    :param options: an object or named tuple containing the options for the
                    web server such as host and port.
    '''
    import os
    from pybald.context import config
    from collections import namedtuple
    from wsgiref.simple_server import make_server
    from pybald.util.static_serve import StaticServer
    if not options:
        defaults = namedtuple('defaults', ['host', 'port'])
        options = defaults('0.0.0.0', 8080)
    # called directly runs a simple dev server
    # add the static server component
    my_app = StaticServer(app, path=os.path.join(config.path, 'public'))
    httpd = make_server(options.host, options.port, my_app)
    stdout.write("Serving on {0}:{1}...\n".format(options.host, options.port))
    httpd.serve_forever()
    sys.exit(1)
