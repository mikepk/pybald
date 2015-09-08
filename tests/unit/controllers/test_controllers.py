import unittest
from pybald.core.controllers import (Controller, action, csrf_protected,
                                     CSRFValidationFailure)
from pybald.core.middleware.sessions import SessionManager
from webob import Request
from six.moves.urllib.parse import urlencode

class MockStash(dict):
    def __call__(self, *pargs, **kargs):
        if not kargs and len(pargs) == 1:
            return self[pargs[0]]
        if kargs:
            self.update(kargs)

class MockSession(object):
    def __init__(self):
        self.stash = MockStash()

class TestControllers(unittest.TestCase):
    def setUp(self):
        import pybald
        context = pybald.configure(config_file="tests/sample_project/project.py")

        class TempController(Controller):
            @action
            @csrf_protected
            def test1(self, req):
                return 'Some data'

        self.controller_class = TempController

    def test_missing_csrf_rejection(self):
        "Reject post to csrf protected action when no CSRF was generated"
        controller = self.controller_class()
        controller.session = MockSession()
        app = controller.test1
        # request.get_response(app)
        # issue a post
        request = Request.blank('/',
                         content_type="application/x-www-form-urlencoded",
                         method="POST",
                         body=urlencode({'__csrf_token__': 'SOMEOTHERTOKEN'}).encode('utf-8'))
        try:
            request.get_response(app)
        except CSRFValidationFailure:
            pass
        else:
            self.fail('Failed to throw validation exception')

    def test_no_csrf_rejection(self):
        "Reject post to csrf protected action w/out token"
        controller = self.controller_class()
        controller.session = MockSession()
        # issue a simulated 'get' to populate the CSRF
        request = Request.blank('/')
        app = controller.test1
        request.get_response(app)
        # issue a post
        request = Request.blank('/',
                         content_type="application/x-www-form-urlencoded",
                         method="POST",
                         body='Nocsrf'.encode('utf-8'))
        try:
            request.get_response(app)
        except CSRFValidationFailure:
            pass
        else:
            self.fail('Failed to throw validation exception')

    def test_wrong_csrf_reject(self):
        "Reject post to csrf protected action w/wrong token"
        controller = self.controller_class()
        controller.session = MockSession()
        # issue a simulated 'get' to populate the CSRF
        request = Request.blank('/')
        app = controller.test1
        request.get_response(app)
        # issue a post with the token
        token = controller.session.stash.get('csrf_token')
        request = Request.blank('/',
                         content_type="application/x-www-form-urlencoded",
                         method="POST",
                         body=urlencode({'__csrf_token__': 'SOMEOTHERTOKEN'}).encode('utf-8'))
        try:
            request.get_response(app)
        except CSRFValidationFailure:
            pass
        else:
            self.fail('Wrong token accepted')

    def test_csrf_accept(self):
        "Accept post to csrf protected action w/token"
        controller = self.controller_class()
        controller.session = MockSession()
        # issue a simulated 'get' to populate the CSRF
        request = Request.blank('/')
        app = controller.test1
        request.get_response(app)
        # issue a post with the token
        token = controller.session.stash.get('csrf_token')
        request = Request.blank('/',
                         content_type="application/x-www-form-urlencoded",
                         method="POST",
                         body=urlencode({'__csrf_token__': token}).encode('utf-8'))
        try:
            request.get_response(app)
        except CSRFValidationFailure:
            self.fail('Correct token not accepted')
        else:
            pass




