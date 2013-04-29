#!/usr/bin/env python
# encoding: utf-8
# """
# Console.py
#
# Created by mikepk on 2011-10-16.
# Copyright (c) 2011 Michael Kowalchik. All rights reserved.
# """
import code
import sys

import readline
import atexit
import os

import project
sys.path.append(project.toplevel)


class Console(code.InteractiveConsole):
    '''Pybald console including history buffer per project.'''
    def __init__(self, project_name, package_name=None):
        import webob
        import pybald
        from pybald.test import Client

        self.project_name = project_name
        if not package_name:
            package_name = self.project_name
        proj_package = '{project}'.format(project=package_name)
        # from project import app, wsgi
        proj = __import__(proj_package, globals(), locals(), ['app', 'wsgi'], -1)
        # from project.app import controllers, models
        __import__('{project}.app.'.format(project=package_name),
                    globals(), locals(), ['controllers', 'models'], -1)
        # from project.wsgi.myapp import app
        __import__('{project}.wsgi.myapp'.format(project=package_name),
                                              globals(), locals(), ['app'], -1)

        # setup console environment for convenience
        console_symbols = proj.wsgi.myapp.__dict__
        console_symbols.update({proj_package: proj})
        console_symbols.update({"models": pybald.db.models})
        console_symbols.update(dict([(i, getattr(proj.app.models, i)) for i
                                                 in proj.app.models.__all__]))
        console_symbols.update(dict([(i, getattr(proj.app.controllers, i)) for i
                                            in proj.app.controllers.__all__]))
        # add webob Req/Resp objects to the console for conv
        console_symbols.update({"Request": webob.Request,
                                "Response": webob.Response})
        console_symbols.update({"c": Client(app=proj.wsgi.myapp.app)})

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
