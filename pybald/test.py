from webob import Request, Response
from urllib import urlencode

import re

class Client(object):
    def __init__(self, app):
        self.app = app
        self.cookies = {}

    def get(self, url):
        req = Request.blank(url)
        for key, value in self.cookies.items():
            req.cookies[key]=value
        resp = req.get_response(self.app)
        # naively handle cookies. This can be made more robust later
        cookie_string = resp.headers.get("set-cookie")
        if cookie_string:
            match = re.search(r'([^\;]*)\;.*', cookie_string)
            if match:
                cookie = match.group(1)
                key, value = match.group(1).split('=')
                self.cookies[key]=value
        return resp

    def clear_cookies(self):
        self.cookies = {}

    def post(self, url, data):
        r = Request.blank(url,
                         content_type="application/x-www-form-urlencoded",
                         method="post",
                         body=urlencode(data))
        return r.get_response(self.app)