import unittest
from mako.template import Template
from webob import Request
import re

not_found_response = '404 Not Found\nContent-Length: 64\nContent-Type: text/plain; charset=UTF-8\n\n404 Not Found\n\nThe resource could not be found.\n\n No URL match  '
general_fault_response = '500 Internal Server Error\nContent-Length: 127\nContent-Type: text/plain; charset=UTF-8\n\n500 Internal Server Error\n\nThe server has either erred or is incapable of performing the requested operation.\n\n General Fault  '
STACK_TRACE = re.compile(r'''500 Internal Server Error\nContent-Type: text/html; charset=UTF-8\nContent-Length: \d+\n\n<html>\n<head>\n    <title>Pybald Runtime Error</title>''')

class TestErrors(unittest.TestCase):
    def setUp(self):
        import pybald
        context = pybald.configure(config_file="tests/sample_project/project.py")
        from tests.sample_project.sample import app

    def test_stack_trace(self):
        "When in debug mode, Exceptions generate stack traces"
        from pybald.context import config
        from tests.sample_project.sample import app
        try:
            resp = Request.blank('/throw_exception').get_response(app)
        except Exception as err:
            self.fail("Exception Generated or Fell Through Error Handler {0}".format(err))
        assert resp.status_code == 500
        assert STACK_TRACE.match(str(resp))

    def test_non_stack_trace(self):
        "When *NOT* in debug mode, Exceptions return generic errors"
        from pybald.context import config
        config.debug = False
        from tests.sample_project.sample import app
        try:
            resp = Request.blank('/throw_exception').get_response(app)
        except Exception as err:
            self.fail("Exception Generated or Fell Through Error Handler {0}".format(err))
        assert resp.status_code == 500
        assert not STACK_TRACE.match(str(resp))
        assert str(resp) == general_fault_response


    def test_404(self):
        "404's are returned properly"
        # from pybald import context
        from tests.sample_project.sample import app
        try:
            resp = Request.blank('/not_there').get_response(app)
        except Exception as err:
            self.fail("Exception Generated or Fell Through Error Handler {0}".format(err))
        print(resp)
        assert resp.status_code == 404
        assert str(resp) == not_found_response
