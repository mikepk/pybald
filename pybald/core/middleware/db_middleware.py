from sqlalchemy.exc import SQLAlchemyError
from pybald.db import models
import sys
from pybald import context


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
            excpt, detail, tb = sys.exc_info()
            context.db.rollback()

            # reraise the original details
            # can't use raw 'raise' because SA + eventlet
            # nukes sys_info
            raise excpt, detail, tb
        else:
            return resp
        finally:
            # always, always, ALWAYS close the session regardless
            # This remove() call has been moved higher in the WSGI stack
            # so that other things needing db sessions can still access the
            # db (like error reporting)
            # models.session.remove()
            context.db.remove()
            del tb

