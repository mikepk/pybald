import unittest
import pybald
expected_sample_fieldset = u'''<div>
<label for="text">Text</label>
  <input id="text" name="text" type="text" value="">
</div>

'''

test_config = dict(env_name="FormTest",
config_object=True,
sample_config=True,
# template_path="tests/sample_project/",
cache_path=None,
# project_name="Sample Project",
debug=True,
template_helpers=['from pybald.core import assets'],
# BUNDLE_SOURCE_PATHS=['tests/sample_project/front_end', 'tests/sample_project/sass'],
path="",
database_engine_uri='sqlite:///:memory:')



# class TestForms(unittest.TestCase):
#     def setUp(self):
#         import pybald
#         context = pybald.configure(config_object=test_config)
#         from pybald.db import models
#         from pybald.core import forms

#         class TestModelForForm(models.Model):
#             text = models.Column(models.Text())

#         class TestForm(forms.BaseForm):
#             text = forms.StringField()

#     def test_create_fieldset(self):
#         '''Create a form fieldset'''
#         fs = TestForm()
#         assert fs.render().__html__() == expected_sample_fieldset

#     def test_bind_data_to_form_and_save(self):
#         '''Create a new model from a form'''
#         models.Model.metadata.create_all()
#         fs = TestForm(data={'text': 'this is totally a test'})
#         if fs.validate():
#             tm = TestModelForForm()
#             fs.populate_obj(tm)
#             tm.save().commit()

#     def test_edit_a_model(self):
#         '''Edit an existing model by rebinding a form / fieldset'''
#         sm = TestModelForForm(text="This is just some sample text already in the model.")
#         sm.save().commit()
#         fs = TestForm(sm, data={'text': 'this is totally a test'})
#         def text_only(value, field):
#             if not (isinstance(value, str)):
#                 raise validators.ValidationError('Value must be text')
#         assert fs.text.value == 'this is totally a test'
#         if fs.validate():
#             fs.model.commit()
#         saved_sample = SampleModel.get(id=1)
#         assert saved_sample.text == 'this is totally a test'

#     def test_validation(self):
#         '''Don't save a model with text value in a numeric validated field'''
#         pass
#         # self.fail('Fix me')
#         # from pybald.core.forms import FieldSet
#         # from pybald.core.forms import validators
#         # from tests.sample_project.sample import SampleModel
#         # def number_only(value, field):
#         #     if not (isinstance(value, int)):
#         #         raise validators.ValidationError('Value must be a number')
#         # fs = FieldSet(SampleModel, data={'SampleModel--text': 'this is totally a test'})
#         # fs.configure(options=[fs.text.validate(number_only)])
#         # if fs.validate():
#         #     fs.model.save().commit()
#         #     self.fail("Model should not have validated")
