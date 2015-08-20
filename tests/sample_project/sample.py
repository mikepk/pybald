import pybald
from pybald.core.controllers import Controller, action
from pybald.core.router import Router
from pybald.db import models
context = pybald.configure(__name__)
from pybald.core.logs import default_debug_log
default_debug_log()

def map(urls):
    urls.connect('home', r'/', controller='hello')

class Test(models.Model):
    t = models.Column(models.Text)

class HelloController(Controller):
    @action
    def index(self, req):
        return "Hello world!"

app = Router(routes=map, controllers=context.controller_registry)
context.start(app)

