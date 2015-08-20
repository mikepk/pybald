import unittest
import pybald
from pybald.core.controllers import Controller
from pybald.db.models import Model

class TestConfig(unittest.TestCase):
    def test_controller_registry(self):
        config_obj = dict(env_name="TestFromObject")
        context = pybald.configure(config_object=config_obj)
        class SampleController(Controller):
            pass
        assert SampleController in Controller.registry

    def test_model_registry(self):
        config_obj = dict(env_name="TestFromObject")
        context = pybald.configure(config_object=config_obj)
        class SampleModel(Model):
            pass
        assert SampleModel in Model.registry

