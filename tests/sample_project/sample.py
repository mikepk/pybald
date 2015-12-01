import pybald
from pybald.core.router import Router
if __name__ == "__main__":
    from pybald.core.logs import default_debug_log
    default_debug_log()
context = pybald.configure(__name__)
from pybald.core.controllers import Controller, action
from pybald.core.middleware.errors import ErrorMiddleware
from pybald.db import models

def map(urls):
    urls.connect('home', r'/', controller='sample')
    urls.connect('variable_test', r'/variable_test/{variable}', controller='sample',
                 action='variable_test')
    # errors
    urls.connect('throw_exception', r'/throw_exception', controller='sample',
                 action='throw_exception')


class SampleModel(models.Model):
    text = models.Column(models.Text)


class SampleController(Controller):
    @action
    def index(self, req):
        self.sample_variable = "Testing"

    @action
    def throw_exception(self, req):
        raise Exception("This is a test exception")


app = Router(routes=map, controllers=context.controller_registry)
app = ErrorMiddleware(app)


if __name__ == "__main__":
    context.start(app)

