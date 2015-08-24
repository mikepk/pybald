import unittest
import pybald
from six.moves.urllib.parse import urlencode
from pybald.core.router import Router
from webob import Request, exc

class TestRouter(unittest.TestCase):
    def setUp(self):
        pybald.configure(config_object={'debug': False})
        def map(urls):
            urls.connect('test1', r'/test1', controller='test1')
            urls.connect('test2', r'/test2', controller='test2', action='index')
            urls.connect('method_test1', r'/method', controller='test2',
                         action='get', conditions=dict(method=["GET"]))
            urls.connect('method_test2', r'/method', controller='test2',
                         action='delete', conditions=dict(method=["DELETE"]))
            urls.connect('test4', r'/test4', controller='test4', action='index')
            urls.redirect('/here', '/there', _redirect_code='302 Found')

        class Test1Controller(object):
            def index(self, environ, start_response):
                start_response('200 OK', [('Content-Type','text/plain')])
                return ["test1"]

        class Test2Controller(object):
            def index(self, environ, start_response):
                start_response('200 OK', [('Content-Type','text/plain')])
                return ["test2"]

            def delete(self, environ, start_response):
                start_response('200 OK', [('Content-Type','text/plain')])
                return ["test2_delete"]

            def get(self, environ, start_response):
                start_response('200 OK', [('Content-Type','text/plain')])
                return ["test2_get"]

        self.app = Router(routes=map, controllers=[Test1Controller, Test2Controller])

    def test_controller_match(self):
        '''Request a URL, match a controller'''
        r = Request.blank('/test1')
        resp = r.get_response(self.app)
        assert resp.body == 'test1'

    def test_no_match(self):
        '''Request a url that doesn't match, throw HTTP Not Found exception'''
        r = Request.blank('/test3')
        try:
            r.get_response(self.app)
        except exc.HTTPNotFound:
            pass

    def test_no_controller_in_registry(self):
        '''Match controller variable but miss on registry'''
        r = Request.blank('/test4')
        try:
            r.get_response(self.app)
        except exc.HTTPNotFound:
            pass

    def test_method_override(self):
        '''Send a `delete` _method data POST, the method is overridden'''
        r = Request.blank('/method',
                         content_type="application/x-www-form-urlencoded",
                         method="POST",
                         body=urlencode({'_method': 'delete'}).encode('utf-8'))
        resp = r.get_response(self.app)
        assert r.method == "DELETE"
        assert resp.body == 'test2_delete'

    def test_not_method_override(self):
        '''Send a `delete` _method url arg as GET, the method is NOT overridden'''
        r = Request.blank('/method?_method=delete')
        resp = r.get_response(self.app)
        assert r.method != "DELETE"
        assert resp.body == 'test2_get'

    def test_redirect(self):
        '''Fetch '/here' and redirect to '/there' '''
        r = Request.blank('/here')
        resp = r.get_response(self.app)
        assert resp.status_code == 302
        assert resp.headers['location'] == 'http://localhost/there'
