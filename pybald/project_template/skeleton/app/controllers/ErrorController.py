from pybald.core.BaseController import action, BaseController
from webob import Response
from pybald.core.errors import pybald_error_template
import project

class Emap(dict):
    def __getitem__(self,key):
        return self.get(key)

    def get(self,key,failobj='general_error'):
        '''Get method defaults to general_error. This is used as the default for missing keys.'''
        if key not in self:
            return failobj
        return super(Emap,self).__getitem__(key)

class ErrorController(BaseController):
    # map status codes to error controller actions
    # Emap object defaults to 'general_error'
    error_map = Emap({404:'not_found',
                 401:'not_authorized',
                 500:'index'})

    @action
    def __call__(self,req):
        '''The ErrorController will return a formatted stack trace if in debug mode, or point to the regular error page otherwise.'''
        if project.email_errors or project.debug:
            stack_trace = pybald_error_template().render(req=req)

        if project.email_errors:
            send_email(stack_trace)

        if project.debug:
            return Response(body=stack_trace, status=500)
        else:
            # call the "vanilla" Error page if we're not in debug mode
            return req.get_response(self.index)


    @action
    def index(self,req):
        self.page['title'] = "We've encountered an error."
        return Response(body=self._view(), status=500)

    @action
    def not_found(self,req):
        # self.page['title'] = "Page not found."
        return Response(body=self._view(), status=404)

    @action
    def not_authorized(self,req):
        # self.page['title'] = "You're not allowed to see this."
        return Response(body=self._view(), status=401)

    @action
    def general_error(self,req):
        return Response(body=self._view())
