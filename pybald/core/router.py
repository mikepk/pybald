#!/usr/bin/env python
# encoding: utf-8
import re
from webob import Request, Response, exc
from routes import Mapper, request_config, URLGenerator
# handle Mako's top level lookup
from mako import exceptions
from pybald.util import camel_to_underscore
import logging
log = logging.getLogger(__name__)


class Router(object):
    # class method match patterns
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

        :param controllers: A registry of all loaded controllers. This is
                            required to do routing lookups. This is also a
                            security precaution since only registered
                            controllers can be matched against.

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
        log.debug(str(self.map))
        self.load(controllers)

    def load(self, controllers):
        '''
        Walks the controller registry and builds the lookup table for
        controller classes to match against.

        Does some text munging to change the camel-case class names into
        underscore-separated url like names. (HomeController to home)

        :param controllers: A controller registry, a list of all controllers
                            that will be used with this application.

        All controller candidates are loaded into a hash to look up
        the matched "controller" urlvar against.

        The _controller suffix is removed from the module name for the url
        route mapping table (so controller="home" matches home_controller).

        This method is called only once at the start of a pybald application.
        '''

        controller_names = []
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
        return "<Router Object>"

    def get_handler(self, urlvars):
        '''Method that returns the callable code mapped to this current
        request.

        This method can be overriden to change the behavior of mapping.
        '''
        controller_name, action_name = urlvars["controller"], urlvars["action"]
        #methods starting with underscore can't be used as actions
        if action_name.startswith("_"):
            raise exc.HTTPNotFound("Invalid Action")

        for key, value in urlvars.items():
            log.debug(u'''{0}: {1}'''.format(key, value))

        try:
            # create controller instance from controllers dictionary
            # using routes 'controller' returned from the match
            controller = self.controllers[controller_name]()
            handler = getattr(controller, action_name)
        # only catch the KeyError/AttributeError for the controller/action
        # search
        except (KeyError, AttributeError):
            raise exc.HTTPNotFound("Missing Controller or Action")

        return handler

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
                log.debug("Changing request method to {0}".format(
                                                        environ["REQUEST_METHOD"]))

        results = self.map.routematch(environ=environ)
        if results:
            urlvars, route = results
        else:
            urlvars, route = {}, None

        url = URLGenerator(self.map, environ)
        config = request_config()

        # Your mapper object
        config.mapper = self.map
        # The dict from m.match for this URL request
        config.mapper_dict = urlvars
        config.host = req.host
        config.protocol = req.scheme
        # defines the redirect method. In this case it generates a
        # Webob Response object with the location and status headers
        # set
        config.redirect = lambda url: Response(location=url, status=302)

        # TODO: routing args is supposed to be pos, key dict
        environ.update({'wsgiorg.routing_args': ((url), urlvars),
                        'routes.route': route,
                        'routes.url': url,
                        'pybald.router': self})

        # Add pybald extension
        # the pybald.extension is a dictionary that can be used to copy state
        # into a running controller (usually handled by the @action decorator)
        environ.setdefault('pybald.extension', {})["url_for"] = url

        # debug print messages
        log.debug('{0:=^79}'.format(' {0} '.format(req.path_qs)))
        log.debug('Method: {0}'.format(req.method))

        # lifted from Routes middleware, handles 'redirect'
        # routes (map.redirect)
        if route and route.redirect:
            route_name = '_redirect_{0}'.format(id(route))
            location = url(route_name, **urlvars)
            return Response(location=location,
                            status=route.redirect_status
                            )(environ, start_response)

        if urlvars:
            handler = self.get_handler(urlvars)
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

