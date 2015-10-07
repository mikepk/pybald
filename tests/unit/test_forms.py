import unittest
import pybald
from pybald.core.forms import validators
from pybald.core.forms import MockParams
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



class TestForms(unittest.TestCase):
    def setUp(self):
        import pybald
        context = pybald.configure(config_object=test_config)

    def tearDown(self):
        from pybald import context
        context._reset()

    def test_create_fieldset(self):
        '''Create a form fieldset'''
        from pybald.core import forms
        from pybald.db import models

        class TestModelForForm(models.Model):
            text = models.Column(models.Text())

        class TestForm(forms.Form):
            text = forms.StringField()

        fs = TestForm()
        assert fs.render().__html__() == expected_sample_fieldset

    def test_bind_data_to_form_and_save(self):
        '''Create a new model from a form'''
        from pybald.core import forms
        from pybald.db import models

        class TestModelForForm(models.Model):
            text = models.Column(models.Text())

        class TestForm(forms.Form):
            text = forms.StringField()

        models.Model.metadata.create_all()
        fs = TestForm(data={'text': 'this is totally a test'})
        if fs.validate():
            tm = TestModelForForm()
            fs.populate_obj(tm)
            tm.save().commit()

    def test_edit_a_model(self):
        '''Edit an existing model by rebinding a form / fieldset'''
        from pybald.core import forms
        from pybald.db import models

        class TestModelForForm(models.Model):
            text = models.Column(models.Text())

        class TestForm(forms.Form):
            text = forms.StringField()

        models.Model.metadata.create_all()
        sm = TestModelForForm(text="This is just some sample text already in the model.")
        sm.save().commit()
        fs = TestForm(formdata=MockParams({'text': 'this is totally a test'}), obj=sm)
        def text_only(value, field):
            if not (isinstance(value, str)):
                raise validators.ValidationError('Value must be text')
        assert fs.text.data == 'this is totally a test'
        if fs.validate():
            fs.populate_obj(sm)
            sm.commit()
        saved_sample = TestModelForForm.get(id=1)
        assert saved_sample.text == 'this is totally a test'

    def test_validation(self):
        '''Fail to validate a form with a text value in an interger numeric validated field'''
        from pybald.core import forms
        from pybald.db import models

        def int_only(value, field):
            if not (isinstance(value, int)):
                raise validators.ValidationError('Value must be a number')

        class TestModelForForm(models.Model):
            text = models.Column(models.Text())

        class TestForm(forms.Form):
            text = forms.StringField('Text', [int_only])


        fs = TestForm(formdata=MockParams({'text': 'this is totally a test'}))
        if fs.validate():
            self.fail("The form validated when it shouldn't have")
        else:
            pass
