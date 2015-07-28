#!/usr/bin/env python
# encoding: utf-8

import unittest

from functools import wraps
# from pybald.core.templates import render as render_view, engine as old_style_render_view
from pybald import app

from webob import Request, Response
from webob import exc
import re
from pybald.util import camel_to_underscore
from routes import redirect_to

import hashlib
import base64
import json
import random

import uuid
import logging
console = logging.getLogger(__name__)

controller_pattern = re.compile(r'(\w+)Controller')


class CSRFValidationFailure(exc.HTTPForbidden):
    pass


def csrf_protected(action_func):
    """
    Decorator to add CSRF (cross-site request forgery) protection to POST
    requests on an action. To use, include this decorator and provide the
    token in any submitted forms.

    For example, in the controller, do:

    @action
    @csrf_protected
    def my_action(self, req):
        ...

    And in the template:

    <form action='my_action' method='post'>
    ${csrf_input}
    ...
    </form>
    """
    CSRF_TOKEN_POST_VARIABLE = '__csrf_token__'

    @wraps(action_func)
    def replacement(self, req):
        if req.method == 'POST':
            try:
                if CSRF_TOKEN_POST_VARIABLE not in req.POST:
                    raise CSRFValidationFailure(
                        ("No %r value found in POST data. Please make sure "
                         "that a ${csrf_input} is used in the form template.")
                        % CSRF_TOKEN_POST_VARIABLE)

                if not self.session.stash.get("csrf_token"):
                    raise CSRFValidationFailure(
                        "CSRF validation failed: no validation token available "
                        "in this session.")

                provided_csrf_token = req.POST.get(CSRF_TOKEN_POST_VARIABLE)

                if provided_csrf_token != self.session.stash.get("csrf_token"):
                    raise CSRFValidationFailure(
                        "CSRF validation failed: token mismatch.")

                else:
                    # success! wipe out the used token
                    self.session.stash(csrf_token=None)
                    #del self.session.csrf_token

            except CSRFValidationFailure:
                # gentle mode, redirect to GET version of the page
                return self._redirect_to(req.path_qs)

        # always stash a new token
        new_token = str(uuid.uuid4()).replace("-", "")
        self.session.stash(csrf_token=new_token)

        self.csrf_input = ("<input type='hidden' name='%s' value='%s' />" % (
            CSRF_TOKEN_POST_VARIABLE, new_token))

        return action_func(self, req)
    return replacement



# a no-op placeholder
def noop_func(*pargs, **kargs):
    '''Do nothing'''
    pass


def get_template_name(instance, method_name):
    '''
    Defines the template id to match against.

    :param instance: the instance to generate a template for
    :param method_name: the method to combine with the instance class

    template path = controller name + '/' + action name, except in the case
    of index. If the template is specified as part of the processed object
    return that, short circuiting any other template name processing

    This form may removed later, considered a candidate for deprecation
    '''
    template_id = getattr(instance, 'template_id', None)
    if template_id:
        return template_id
    # build a default template name if one isn't explicitly set
    try:
        template_root_name = camel_to_underscore(
                  controller_pattern.search(instance.__class__.__name__
                                            ).group(1))
    except AttributeError:
        template_root_name = ''
    return "/".join(filter(None, [template_root_name, method_name]))


# action / method decorator
def action(method):
    '''
    Decorates methods that are WSGI apps to turn them into pybald-style actions.

    :param method: A method to turn into a pybald-style action.

    This decorator is usually used to take the method of a controller instance
    and add some syntactic sugar around it to allow the method to use WebOb
    Request and Response objects. It will work with any method that
    implements the WSGI spec.

    It allows actions to work with WebOb request / response objects and handles
    default behaviors, such as displaying the view when nothing is returned,
    or setting up a plain text Response if a string is returned. It also
    assigns instance variables from the ``pybald.extension`` environ variables
    that can be set from other parts of the WSGI pipeline.

    This decorator is optional but recommended for making working
    with requests and responses easier.
    '''
    # the default template name is the controller class + method name
    # the method name is pulled during decoration and stored for use
    # in template lookups
    template_name = method.__name__
    # special case where 'call' or 'index' use the base class name
    # for the template otherwise use the base name
    if template_name in ('index', '__call__'):
        template_name = ''

    @wraps(method)
    def action_wrapper(self, environ, start_response):
        req = Request(environ)
        # add any url variables as members of the controller
        for varname, value in req.urlvars.items():
            # Set the controller object to contain the url variables
            # parsed from the dispatcher / router
            setattr(self, varname, value)

        # add the pybald extension dict to the controller
        # object
        for key, value in req.environ.setdefault('pybald.extension', {}).items():
            setattr(self, key, value)

        # TODO: fixme this is a hack
        setattr(self, 'request', req)
        setattr(self, 'request_url', req.url)

        # set pre/post/view to a no-op if they don't exist
        pre = getattr(self, '_pre', noop_func)
        post = getattr(self, '_post', noop_func)

        # set the template_id for this request
        self.template_id = get_template_name(self, template_name)

        # The response is either the controllers _pre code, whatever
        # is returned from the controller
        # or the view. So pre has precedence over
        # the return which has precedence over the view
        resp = (pre(req) or
                 method(self, req) or
                 app.render(template=self.template_id,
                             data=self.__dict__ or {}))
        # if the response is currently a string
        # wrap it in a response object
        if isinstance(resp, basestring):
            resp = Response(body=resp, charset="utf-8")
        # run the controllers post code
        post(req, resp)
        return resp(environ, start_response)
    return action_wrapper


# def caching_pre(keys, method_name, prefix=''):
#     '''Decorator for pybald _pre to return cached responses if available.'''
#     if keys is None:
#         keys = []

#     def pre_wrapper(pre):
#         def replacement(self, req):
#             val = ":".join([prefix] + [str(getattr(self, k, '')) for
#                         k in keys] + [method_name])
#             self.cache_key = base64.urlsafe_b64encode(hashlib.md5(val).digest())
#             resp = project.mc.get(self.cache_key)
#             if resp:
#                 return resp
#             return pre(req)
#         return replacement
#     return pre_wrapper


# def caching_post(time=0):
#     '''Decorator for pybald _post to cache/store responses.'''
#     def post_wrapper(post):
#         def replacement(self, req, resp):
#             post(req, resp)
#             # only cache 2XX or 4XX responses
#             if (200 <= resp.status_code < 300) or (400 <= resp.status_code < 500):
#                 if 'X-Cache' not in resp.headers:
#                     resp.headerlist.append(('X-Cache', 'MISS'))
#                     project.mc.set(self.cache_key, resp, time)
#                 else:
#                     resp.headers['X-Cache'] = 'HIT'
#         return replacement
#     return post_wrapper

# regenerate a content_cache_prefix on every reload so that content will
# be force loaded after any full application restart
# This provides a way to cache static content for the duration of the
# application lifespan.
content_cache_prefix = hex(random.randrange(0, 2 ** 32 - 1))


# memcache for actions
def action_cached(prefix=content_cache_prefix, keys=None, time=0):
    '''
    Wrap actions and return pre-generated responses when appropriate.
    '''
    if keys is None:
        keys = []

    # def cached_wrapper(my_action_method):
    #     @wraps(my_action_method)
    #     def replacement(self, environ, start_response):
    #         # bind newly wrapped methods to self
    #         self._pre = caching_pre(keys,
    #                                 my_action_method.__name__,
    #                                 prefix=prefix)(self._pre
    #                                     ).__get__(self, self.__class__)
    #         self._post = caching_post(time)(self._post
    #                                     ).__get__(self, self.__class__)
    #         return my_action_method(self, environ, start_response)
    #     # don't enable caching if requested
    #     if project.DISABLE_STATIC_CONTENT_CACHE:
    #         return my_action_method
    #     return replacement
    # return cached_wrapper

from pybald.app import class_registry
class RegistryMount(type):
    '''
    A registry creating metaclass that keeps track of all defined classes that
    inherit from a base class using this metaclass.
    '''
    # lifted almost verbatim from: http://martyalchin.com/2008/jan/10/simple-plugin-framework/
    def __init__(cls, name, bases, attrs):
        try:
            cls.registry.append(cls)
        except AttributeError:
            # this is processing the first class (the mount point)
            cls.registry = class_registry

        return super(RegistryMount, cls).__init__(name, bases, attrs)


class Controller(object):
    '''Base controller that includes the view and a default index method.'''
    __metaclass__ = RegistryMount

    def __init__(self, *pargs, **kargs):
        for key, value in kargs.items():
            setattr(self, key, value)

    def _pre(self, req):
        pass

    def _post(self, req, resp):
        pass

    def _redirect_to(self, *pargs, **kargs):
        '''Redirect the controller'''
        return redirect_to(*pargs, **kargs)

    def _not_found(self, text=None):
        '''Raise the 404 http_client_error exception.'''
        raise exc.HTTPNotFound(text)

    def _status(self, code):
        '''Raise an http_client_error exception using a specific code'''
        raise exc.status_map[int(code)]

    def _JSON(self, data, status=200):
        '''Return JSON object with the proper-ish headers.'''
        res = Response(body=json.dumps(data),
            status=status,
            # wonky Cache-Control headers to stop IE6 from caching content
            cache_control="max-age=0,no-cache,no-store,post-check=0,pre-check=0",
            expires="Mon, 26 Jul 1997 05:00:00 GMT",
            content_type="application/json",
            charset='UTF-8'
            )
        return res

    # def _view(self, data=None):
    #     '''
    #     This method is a shim between the old view rendering code and the new
    #     template rendering methods. It should not be used and is present only
    #     to maintain backward compatibility.

    #     This is targeted for deprecation.
    #     '''
    #     return old_style_render_view(data or self.__dict__ or {})

    # _render_view = render_view

# alias for backwards copatibility
BaseController = Controller


class BaseControllerTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
