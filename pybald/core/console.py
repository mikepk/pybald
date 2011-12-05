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
        self.project_name = project_name
        if not package_name:
            package_name = self.project_name

        import pybald
        # from pybald.core.console import Console
        from pybald.test import Client
        proj_package = '{project}'.format(project=package_name)
        proj = __import__(proj_package, globals(), locals(), ['app','wsgi'],
                                                                            -1)
        __import__('{project}.app.models'.format(project=package_name))
        __import__('{project}.app.controllers'.format(project=package_name))
        __import__('{project}.wsgi.myapp'.format(project=package_name),
                                              globals(), locals(), ['app'], -1)
        c = Client(app=proj.wsgi.myapp.app)
        import webob
        # setup console environment for convenience
        console_symbols = proj.wsgi.myapp.__dict__
        console_symbols.update({"models":pybald.db.models})
        console_symbols.update(proj.app.models.__dict__)
        console_symbols.update(proj.app.controllers.__dict__)

        # console_symbols.update(quiz_site.app.controllers.__dict__)
        console_symbols.update({"Request":webob.Request,
                             "Response":webob.Response})
        console_symbols.update({"c":c})

        histfile=os.path.expanduser("~/.pybald-{0}-console-history".format(project_name))

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
        # console = Console(locals=console_symbols)
        self.interact('''Welcome to the pybald interactive console
 ** project:{0} **
'''.format(self.project_name))