import pybald
from pybald.core.controllers import Controller, action
from pybald.core.router import Router
from pybald.db import models
context = pybald.configure(__name__)

def map(urls):
    urls.connect('home', r'/', controller='sample')

class SampleModel(models.Model):
    text = models.Column(models.Text)

class SampleController(Controller):
    @action
    def index(self, req):
        pass

app = Router(routes=map, controllers=context.controller_registry)

if __name__ == "__main__":
    from pybald.core.logs import default_debug_log
    default_debug_log()
    context.start(app)

