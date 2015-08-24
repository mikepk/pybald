import unittest


class TestOrm(unittest.TestCase):
    def setUp(self):
        import pybald
        context = pybald.configure(config_file="tests/sample_project/project.py")
        from tests.sample_project.sample import app
        from pybald.db.models import Model
        Model.metadata.create_all()

    def test_model_save(self):
        "Save a model"
        from tests.sample_project.sample import SampleModel
        test_model = SampleModel(text="This is just the first test")
        try:
            test_model.save().commit()
        except Exception as err:
            self.fail("Model save failed: {0}".format(err))

    def test_model_save_load(self):
        "Read back a model after saving it"
        from tests.sample_project.sample import SampleModel
        test_model = SampleModel(text="This is just a test")
        test_model.save().commit()
        test_model_read = SampleModel.get(id=1)
        assert test_model_read.text == "This is just a test"



