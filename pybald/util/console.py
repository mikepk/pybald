#!/usr/bin/env python
# encoding: utf-8
# """
# Console.py
#
# Created by mikepk on 2014-10-16.
# Copyright (c) 2015 Michael Kowalchik. All rights reserved.
# """
import code

import readline
import atexit
import os

import webob
from ..test import Client


class Console(code.InteractiveConsole):
    '''Pybald console including history buffer per project.'''
    def __init__(self, project_name, package_name=None, app=None,
                 additional_symbols=None):
        if additional_symbols is None:
            additional_symbols = {}

        self.project_name = project_name
        if not package_name:
            package_name = self.project_name

        # add the application to the console namespace
        console_symbols = {'app': app}

        # add webob Req/Resp objects to the console for convenience
        console_symbols.update({"Request": webob.Request,
                                "Response": webob.Response})
        console_symbols.update({"c": Client(app=app)})
        console_symbols.update(additional_symbols)

        histfile = os.path.expanduser("~/.pybald-{0}-console-history".format(
                                                                 project_name))

        code.InteractiveConsole.__init__(self, locals=console_symbols,
                                                          filename="<console>")
        self.init_history(histfile)

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.write_history_file(histfile)

    def run(self):
        # Fire up the console with the project, controllers, and models defined.
        self.interact('''Welcome to the pybald interactive console\n'''
                      ''' ** project: {0} **'''.format(self.project_name))


def start_console(app):
    '''Start a console with a particular app.

    :app: A wsgi application.

    A pybald application must be configured before starting a console.
    '''
    import pybald
    from pybald.db import models
    # now the models registry is loaded and the additional_symbols
    # added so models are available in the console
    from pybald.db.models import Model
    symbols = dict([(model.__name__, model) for model in Model.registry])
    symbols['models'] = models
    symbols['db'] = pybald.app.db
    # create a pybald console around it
    console = Console(project_name=pybald.app.name, app=app,
                      additional_symbols=symbols)
    console.run()