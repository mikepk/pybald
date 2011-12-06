from pybald.core.controllers import action, BaseController
class HomeController(BaseController):
    '''The Home page.'''

    @action
    def index(self, req):
        return "Pybald is working."
