'''
Test Module for pybald including a simple client for issuing web-like
requests against the WSGI application pipeline.
'''
from webob import Request
from six.moves.urllib.parse import urlencode

import re

class Client(object):
    '''Web testing client for pybald'''
    def __init__(self, app):
        self.app = app
        self.cookies = {}

    def _set_cookie(self, set_cookie):
        '''Naively sets cookies for this test client session'''
        match = re.search(r'([^\;]*)\;.*', set_cookie)
        if match:
            # cookie = match.group(1)
            key, value = match.group(1).split('=')
            self.cookies[key] = value

    def get(self, url):
        '''Issue a GET request directly against the WSGI pybald app'''
        req = Request.blank(url)
        for key, value in self.cookies.items():
            req.cookies[key] = value
        resp = req.get_response(self.app)
        # naively handle cookies. This can be made more robust later
        cookie_string = resp.headers.get("set-cookie")
        if cookie_string:
            self._set_cookie(cookie_string)
        return resp

    def clear_cookies(self):
        '''Delete all cookies from this session.'''
        self.cookies = {}

    def post(self, url, data):
        '''Issue a POST request directly against the WSGI pybald app'''
        req = Request.blank(url,
                         content_type="application/x-www-form-urlencoded",
                         method="POST",
                         body=urlencode(data))
        for key, value in self.cookies.items():
            req.cookies[key] = value

        resp = req.get_response(self.app)
        # naively handle cookies. This can be made more robust later
        cookie_string = resp.headers.get("set-cookie")
        if cookie_string:
            self._set_cookie(cookie_string)

        return resp
