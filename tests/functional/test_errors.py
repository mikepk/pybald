import unittest
from webob import Request
import re
import pybald
from pybald import context
from pybald.core.router import Router
from pybald.core.controllers import Controller, action
from pybald.core.middleware.errors import ErrorMiddleware

not_found_response = '404 Not Found\nContent-Length: 64\nContent-Type: text/plain; charset=UTF-8\n\n404 Not Found\n\nThe resource could not be found.\n\n No URL match  '
general_fault_response = '500 Internal Server Error\nContent-Length: 127\nContent-Type: text/plain; charset=UTF-8\n\n500 Internal Server Error\n\nThe server has either erred or is incapable of performing the requested operation.\n\n General Fault  '
STACK_TRACE = re.compile(r'''500 Internal Server Error\nContent-Type: text/html; charset=UTF-8\nContent-Length: \d+\n\n<html>\n<head>\n    <title>Pybald Runtime Error</title>''')

def map(urls):
    urls.connect('home', r'/', controller='sample')
    urls.connect('variable_test', r'/variable_test/{variable}', controller='sample',
                 action='variable_test')
    # errors
    urls.connect('throw_exception', r'/throw_exception', controller='sample',
                 action='throw_exception')

class SampleController(Controller):
    @action
    def index(self, req):
        self.sample_variable = "Testing"

    @action
    def throw_exception(self, req):
        raise Exception("This is a test exception")


test_conf = dict(database_engine_uri='sqlite:///:memory:',
                 env_name="SampleTestProjectEnvironment",
                 debug=True)


class TestErrors(unittest.TestCase):
    def setUp(self):
        context._reset()


    def tearDown(self):
        context._reset()

    def test_stack_trace(self):
        "When in debug mode, throw an Exception and generate a stack trace"
        pybald.configure(config_object=test_conf)
        app = Router(routes=map, controllers=[SampleController])
        app = ErrorMiddleware(app)

        try:
            resp = Request.blank('/throw_exception').get_response(app)
        except Exception as err:
            self.fail("Exception Generated or Fell Through Error Handler {0}".format(err))
        assert resp.status_code == 500
        assert STACK_TRACE.match(str(resp))

    def test_non_stack_trace(self):
        "When *NOT* in debug mode, throw an Exception and return a generic error"
        test_w_debug_conf = test_conf.copy()
        test_w_debug_conf.update(dict(debug=False))
        pybald.configure(config_object=test_w_debug_conf)
        app = Router(routes=map, controllers=[SampleController])
        app = ErrorMiddleware(app)
        try:
            resp = Request.blank('/throw_exception').get_response(app)
        except Exception as err:
            self.fail("Exception Generated or Fell Through Error Handler {0}".format(err))
        assert resp.status_code == 500
        assert not STACK_TRACE.match(str(resp))
        assert str(resp) == general_fault_response


    def test_404(self):
        "Return a 404 response"
        pybald.configure(config_object=test_conf)
        app = Router(routes=map, controllers=[SampleController])
        app = ErrorMiddleware(app)
        try:
            resp = Request.blank('/not_there').get_response(app)
        except Exception as err:
            self.fail("Exception Generated or Fell Through Error Handler {0}".format(err))
        print(resp)
        assert resp.status_code == 404
        assert str(resp) == not_found_response
