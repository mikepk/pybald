import unittest
import pybald
from pybald import context

class TestOrm(unittest.TestCase):
    def setUp(self):
        context._reset()
        pybald.configure(config_object=dict(database_engine_uri='sqlite:///:memory:'))

    def tearDown(self):
        context._reset()

    def test_model_save(self):
        "Save a model"
        from pybald.db import models

        class SampleModel(models.Model):
            text = models.Column(models.Text)

        models.Model.metadata.create_all()
        test_model = SampleModel(text="This is just the first test")
        try:
            test_model.save().commit()
        except Exception as err:
            self.fail("Model save failed: {0}".format(err))

    def test_model_save_load(self):
        "Read back a model after saving it"
        from pybald.db import models

        class SampleModel(models.Model):
            text = models.Column(models.Text)

        models.Model.metadata.create_all()
        test_model = SampleModel(text="This is just a test")
        test_model.save().commit()
        test_model_read = SampleModel.get(id=1)
        assert test_model_read.text == "This is just a test"



