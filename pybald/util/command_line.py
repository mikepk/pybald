import argparse
from pybald.util.console import start_console
from pybald.util.dev_server import start_dev_server
def start(app):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest="subcommand")
    subparsers.required = True
    parser_console = subparsers.add_parser('console', help='console help')
    parser_console.set_defaults(run=start_console)
    parser_serve = subparsers.add_parser('serve', help='serve help')
    parser_serve.add_argument('--host', type=str)
    parser_serve.add_argument('--port', type=int)
    parser_serve.set_defaults(host='0.0.0.0', port=8080)
    parser_serve.set_defaults(run=start_dev_server)
    options = parser.parse_args()
    options.run(app, options)