import unittest
import pybald
from pybald.core.controllers import Controller
from pybald.db import models
from pybald import context

class TestRegistries(unittest.TestCase):
    def setUp(self):
        config_obj = dict(env_name="TestFromObject",
                          database_engine_uri='sqlite:///:memory:')
        pybald.configure(config_object=config_obj)

    def tearDown(self):
        context._reset()

    def test_controller_registry(self):
        "Create a controller, it appears in the Controller registry"
        class AnotherSampleController(Controller):
            pass
        assert AnotherSampleController in Controller.registry

    def test_model_registry(self):
        "Create a model, it appears in the Model registry"
        class AnotherSampleModel(models.Model):
            pass
        assert AnotherSampleModel in models.Model.registry

