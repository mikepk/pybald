from pybald.core.BaseController import action, BaseController

class HomeController(BaseController):
    '''A simple controller object'''

    @action
    def index(self, req):
        '''Home switch between logged in and logged out.'''
        pass

