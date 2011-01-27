from pybald.core.BaseController import action, BaseController

class ContentController(BaseController):
    @action
    def index(self,req):
        pass

    @action
    def render(self,req):
        self.template_id = 'content/%s' % self.template
