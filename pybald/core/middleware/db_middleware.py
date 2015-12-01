import sys
from six import reraise as raise_
from sqlalchemy.exc import SQLAlchemyError
from pybald import context
from webob import Response
import logging
log = logging.getLogger(__name__)

class EndPybaldMiddleware(object):
    '''Utilitiy middleware to force remove current session at the end of
    the request.'''
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        try:
            return self.application(environ, start_response)
        finally:
            # always, always, ALWAYS close the session regardless
            context.db.remove()


class DbMiddleware(object):
    '''The database middleware provides three behaviors, committing
    transactions at the end of the request, rolling back database transactions
    if errors occur and forcibly closing the session
    at the end of the web request to avoid dangling connections.'''
    def __init__(self, application=None):
        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()

    def __call__(self, environ, start_response):
        # req = Request(environ)
        tb = None
        #pass through if no exceptions occur, commit sessions on complete
        try:
            resp = self.application(environ, start_response)
            # commit any outstanding sql
            context.db.commit()
        # on any SQLAlchemy Errors, rollback the transaction
        except SQLAlchemyError:
            # This pattern can cause memory leaks, so hopefully db errors
            # will be scrubbed from the code so this won't be hit
            log.exception("SQLAlchemy Error")
            excpt, detail, tb = sys.exc_info()
            context.db.rollback()
            # reraise the original details
            # can't use raw 'raise' because SA + eventlet
            # nukes sys_info
            raise_(excpt, detail, tb)
        else:
            return resp
        finally:
            # always, always, ALWAYS close the session regardless
            context.db.remove()
            del tb

