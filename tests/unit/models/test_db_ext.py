import unittest
import pybald
from pybald import context
import sqlalchemy.exc


class TestDbExt(unittest.TestCase):
    def setUp(self):
        context._reset()
        pybald.configure(config_object=dict(database_engine_uri='sqlite:///:memory:'))

    def tearDown(self):
        context._reset()

    def test_ascii_type_rejects_non_ascii(self):
        "ASCII type throws error on non-ascii data"
        from pybald.db import models

        class SampleModel(models.Model):
            text = models.Column(models.ASCII)

        models.Model.metadata.create_all()
        test_model = SampleModel(text=u"¡This is just the first test!")
        with self.assertRaises(sqlalchemy.exc.StatementError) as context:
            test_model.save().commit()

    def test_ascii_type(self):
        "ASCII type accepts unicode that can be encoded in ASCII"
        from pybald.db import models

        class SampleModel(models.Model):
            text = models.Column(models.ASCII)

        models.Model.metadata.create_all()
        test_model = SampleModel(text=u"This is just the first test!")
        test_model.save().commit()

    def test_save_json_type(self):
        "JSON type accepts dicts and stores JSON"
        from pybald.db import models

        class SampleModel(models.Model):
            data = models.Column(models.JSONEncodedDict)

        models.Model.metadata.create_all()
        test_model = SampleModel(data={"A": 1, "B": 2})
        test_model.save().commit()

    def test_read_json_type(self):
        "JSON type reads JSON from db and returns dict"
        from pybald.db import models

        class SampleModel(models.Model):
            data = models.Column(models.JSONEncodedDict)

        models.Model.metadata.create_all()
        test_model = SampleModel(data={"A": 1, "B": 2})
        test_model.save().commit()

        test_model_read = SampleModel.get(id=1)
        print(test_model_read.data)
        self.assertEqual(test_model_read.data, {"A": 1, "B": 2})

    def test_save_zip_pickle(self):
        from pybald.db import models

        class SampleModel(models.Model):
            data = models.Column(models.ZipPickleType)

        models.Model.metadata.create_all()
        test_model = SampleModel(data={"A": 1, "B": 2})
        test_model.save().commit()

    def test_read_zip_pickle(self):
        from pybald.db import models

        class SampleModel(models.Model):
            data = models.Column(models.ZipPickleType)

        models.Model.metadata.create_all()
        test_model = SampleModel(data={"A": 1, "B": 2})
        test_model.save().commit()

        test_model_read = SampleModel.get(id=1)
        self.assertEqual(test_model_read.data, {"A": 1, "B": 2})

    def test_mutation_dict(self):
        from pybald.db import models

        class SampleModel(models.Model):
            data = models.Column(models.MutationDict.as_mutable(models.JSONEncodedDict))

        models.Model.metadata.create_all()
        test_model = SampleModel(data={"A": 1, "B": 2})
        test_model.save().commit()
        # not changed
        self.assertNotIn(test_model, context.db.dirty)
        test_model.data["C"] = 3
        # now it *is* changed
        self.assertIn(test_model, context.db.dirty)
        test_model.commit()
        # changes saved
        self.assertNotIn(test_model, context.db.dirty)

        del test_model.data["A"]
        self.assertIn(test_model, context.db.dirty)
        test_model.commit()
        self.assertNotIn(test_model, context.db.dirty)

        test_model.data.update({"D": 4, "E": 5})
        self.assertIn(test_model, context.db.dirty)
        test_model.commit()
        self.assertNotIn(test_model, context.db.dirty)

        test_model.data.pop("B")
        self.assertIn(test_model, context.db.dirty)
        test_model.commit()
        self.assertNotIn(test_model, context.db.dirty)

        test_model.data.popitem()
        self.assertIn(test_model, context.db.dirty)
        test_model.commit()
        self.assertNotIn(test_model, context.db.dirty)