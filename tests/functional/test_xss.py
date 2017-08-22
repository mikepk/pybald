import unittest
from webob import Request
import pybald
from pybald import context
from pybald.core.router import Router
from pybald.core.controllers import Controller, action
from pybald.core.middleware.errors import ErrorMiddleware

import logging
log = logging.getLogger(__name__)


def map(urls):
    # errors
    urls.connect('test_xss_url_param', r'/test_xss_url_param', controller='xss',
                 action='test_url_param')


class XssController(Controller):
    @action
    def test_url_param(self, req):
        template = '''
<div>${url_param}</div>
'''
        data = {'url_param': req.GET['url_parameter']}
        return context.render.raw_template(template, data)


test_conf = dict(database_engine_uri='sqlite:///:memory:',
                 env_name="SampleTestProjectEnvironment",
                 debug=True)


class TestXss(unittest.TestCase):
    def setUp(self):
        context._reset()

    def tearDown(self):
        context._reset()

    def test_url_param_injection(self):
        '''Test that rendering a url parameter escapes any dangerous html'''
        pybald.configure(config_object=test_conf)
        app = Router(routes=map, controllers=[XssController])
        app = ErrorMiddleware(app)

        resp = Request.blank('/test_xss_url_param?url_parameter=%3C/script%3E%3Cscript%3Ealert%28document.cookie%29%3C/script%3E').get_response(app)
        self.assertEqual(resp.body,
                        b'\n<div>&lt;/script&gt;&lt;script&gt;alert(document.cookie)&lt;/script&gt;</div>\n')


if __name__ == "__main__":
    unittest.main()
