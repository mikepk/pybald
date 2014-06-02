#!/usr/bin/env python
# encoding: utf-8

import unittest
import re
from webob import Request, Response, exc
from routes import Mapper, request_config, URLGenerator
# handle Mako's top level lookup
from mako import exceptions
from pybald.util import camel_to_underscore
import logging
console = logging.getLogger(__name__)


class Router(object):
    # class method match patterns
    has_underscore = re.compile(r'^\_')
    controller_pattern = re.compile(r'(\w+)_controller')

    # add controllers=None to the call sig and use that for controller
    # loading
    def __init__(self, application=None, routes=None, controllers=None):
        '''
        Create a Router object, the core of the pybald framework.

        :param application:  WSGI application/middleware that is to be
                             *wrapped* by the router in the web app pipeline.

        :param routes: A routing function that takes a mapper (for parsing and
                       matching urls).

        '''
        if routes is None or not callable(routes):
            raise TypeError("Route mapping is required. Please pass in a "
                            "routing function to the router as an arg to "
                            "Router init. "
                            "The routing function takes a routes mapper "
                            "object and uses it to contruct url mappings. "
                            "See pybald docs for more details.")

        self.controllers = {}
        # initialize Router
        # explicit turns off route memory and 'index' for
        # default action
        self.map = Mapper(explicit=False)
        routes(self.map)
        # debug print the whole URL map
        console.debug(str(self.map))
        if controllers is None:
            self.load_old_style()
        else:
            self.load(controllers)

    def load_old_style(self):
        '''Compatibility method for old-style pybald install.'''
        console.warn("!"*80+'''
!! Old style Router init is deprecated.
!!
!! New style pybald Router objects are constructed by passing in the controller
!! module or controller registry.
!! You will want to update your wsgi/myapp.py file.
!! app = Router(controllers=CONTROLLER_REGISTRY)
'''+"!"*80)
        import project
        # load the controllers from the project defined path
        # change this to passed in value to the Router. That way it can
        # be project specific
        # Load the project specified in the project file
        my_project = __import__(project.package_name, globals(), locals(),
                                                                    ['app'], -1)
        # add the project package name to the global symbol table
        # to avoid any double imports
        globals()[project.package_name] = my_project
        # import all controllers
        __import__('{project}.app'.format(project=project.package_name),
                              globals(), locals(), ['controllers'], -1)
        self.load(my_project.app.controllers)

    def load(self, controllers):
        '''
        Finds registred controllers in controllers. Does some text
        munging to change the camel-case class names into
        underscore-separated url like names. (HomeController to home)

        :param controllers: A module containing all loaded controllers

        All controller candidates are loaded into a hash to look up
        the matched "controller" urlvar against.

        The _controller suffix is removed from the module name for the url
        route mapping table (so controller="home" matches home_controller).

        against and the routes regex is initialized with a list of controller
        names.

        Called only once at the start of a pybald application.
        '''

        controller_names = []
        # switch between old-style package container and registry model
        # both should work here
        if hasattr(controllers, '__all__'):
            controller_iterator = ((name, getattr(controllers, name)) for
                                   name in controllers.__all__)
        else:
            controller_iterator = ((controller.__name__, controller) for
                                   controller in controllers)
        for name, controller in controller_iterator:
            controller_name = camel_to_underscore(name)
            try:
                controller_path_name = self.controller_pattern.search(
                                                    controller_name).group(1)
            except AttributeError:
                controller_path_name = controller_name
            controller_names.append(controller_path_name)
            # self.controllers holds paths to map to modules and controller
            # names
            self.controllers[controller_path_name] = controller

        # register the controller module names
        # with the mapper, creates the internal regular
        # expressions
        self.map.create_regs(controller_names)

    def __repr__(self):
        return "<Pybald Router Object>"

    def get_handler(self, urlvars=None):
        controller_name, action_name = urlvars["controller"], urlvars["action"]

        #methods starting with underscore can't be used as actions
        if self.has_underscore.match(action_name):
            raise exc.HTTPNotFound("Invalid Action")

        for key, value in urlvars.items():
            console.debug(u'''{0}: {1}'''.format(key, value))

        try:
            # create controller instance from controllers dictionary
            # using routes 'controller' returned from the match
            controller = self.controllers[controller_name]()
            handler = getattr(controller, action_name)
        # only catch the KeyError/AttributeError for the controller/action
        # search
        except (KeyError, AttributeError):
            raise exc.HTTPNotFound("Missing Controller or Action")

        return controller, handler

    def __call__(self, environ, start_response):
        '''
        A Router instance is a WSGI app. It accepts the standard WSGI call
        signature of ``environ``, ``start_response``.

        The Router has a few jobs. First it uses the Routes package to
        compare the requested path to available url patterns that have
        been loaded and passed to the Router upon init.

        Router is the most *framework-like* component of Pybald. In addition to
        dispatching urls to controllers, it also allows 'method override'
        behavior allowing other HTTP methods to be invoked such as ``put`` and
        ``delete`` from web clients that don't support them natively.

        :param environ: WSGI CGI-like request environment

        :param start_response: WSGI callback for starting the response and
        setting HTTP response headers
        '''
        req = Request(environ)
        req.errors = 'ignore'
        #method override
        #===============
        # for REST architecture, this allows a POST parameter of _method
        # to be used to override POST with alternate HTTP verbs (PUT, DELETE)
        if req.POST:
            override_method = req.POST.pop('_method', None)
            if override_method is not None:
                environ['REQUEST_METHOD'] = override_method.upper()
                console.debug("Changing request method to {0}".format(
                                                        environ["REQUEST_METHOD"]))

        results = self.map.routematch(environ=environ)
        if results:
            match, route = results[0], results[1]
        else:
            match = route = None

        url = URLGenerator(self.map, environ)
        config = request_config()

        # Your mapper object
        config.mapper = self.map
        # The dict from m.match for this URL request
        config.mapper_dict = match
        config.host = req.host
        config.protocol = req.scheme
        # host_port
        # defines the redirect method. In this case it generates a
        # Webob Response object with the location and status headers
        # set
        config.redirect = lambda url: Response(location=url, status=302)

        environ.update({'wsgiorg.routing_args': ((url), match),
                        'routes.route': route,
                        'routes.url': url,
                        'pybald.router': self})

        # Add pybald extension
        # the pybald.extension is a dictionary that can be used to copy state
        # into a running controller (usually handled by the @action decorator)
        environ.setdefault('pybald.extension', {})["url_for"] = url

        # debug print messages
        console.debug('{0:=^79}'.format(' {0} '.format(req.path_qs)))
        console.debug('Method: {0}'.format(req.method))

        # use routes to match the url to a path
        # urlvars will contain controller + other non query string
        # URL data. Middleware above this can override and set urlvars
        # and the router will use those values.
        # TODO: allow individual variable overrides?
        urlvars = environ.get('urlvars', match) or {}

        # lifted from Routes middleware, handles 'redirect'
        # routes (map.redirect)
        if route and route.redirect:
            route_name = '_redirect_{0}'.format(id(route))
            location = url(route_name, **match)
            return Response(location=location,
                            status=route.redirect_status
                            )(environ, start_response)

        req.urlvars = urlvars
        environ['urlvars'] = urlvars

        if urlvars:
            controller, handler = self.get_handler(urlvars)
        # No URL vars means nothing matched in the mapper function
        else:
            raise exc.HTTPNotFound("No URL match")

        try:
            # call the action we determined from the mapper
            return handler(environ, start_response)
        # This is a mako 'missing template' exception
        except exceptions.TopLevelLookupException:
            raise exc.HTTPNotFound("Missing Template")
        # All other program errors are allowed to bubble up
        # e.g. a 500 server error


class routerTests(unittest.TestCase):
    def setUp(self):
        pass

    def testMap(self):
        router = Router()

    def testRoute(self):
        pass

    def testLoad(self):
        pass

if __name__ == '__main__':
    unittest.main()
