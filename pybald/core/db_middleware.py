from webob import Request, Response
from sqlalchemy.exc import SQLAlchemyError
from pybald.db import models
import sys
class DbMiddleware(object):
    def __init__(self,application=None):
        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()

    def __call__(self,environ,start_response):
        req = Request(environ)
        tb = None
        #pass through if no exceptions occur, commit sessions on complete
        try:
            resp = req.get_response(self.application)(environ,start_response)
        # on any SQLAlchemy Errors, rollback the transaction
        except SQLAlchemyError, err:
            # This pattern can cause memory leaks, so hopefully db errors
            # will be scrubbed from the code so this won't be hit
            excpt, detail, tb = sys.exc_info()
            models.session.rollback()
            # reraise the original details
            # can't use raw 'raise' because SA + eventlet
            # nukes sys_info
            return err(environ,start_response)
            raise excpt, detail, tb
        else:
            # commit any outstanding sql,
            models.session.commit()
            return resp
        finally:
            # always close the session
            models.session.remove()
            del tb
