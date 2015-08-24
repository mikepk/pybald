import unittest
import pybald
expected_sample_fieldset = u'''
<div>
  <label class="field_opt" for="SampleModel--text">Text</label>
  <input id="SampleModel--text" name="SampleModel--text" type="text" />

</div>

'''

class TestForms(unittest.TestCase):
    def setUp(self):
        import pybald
        context = pybald.configure(config_file="tests/sample_project/project.py")
        from tests.sample_project.sample import app
        from pybald.db.models import Model
        Model.metadata.create_all()

    def test_create_fieldset(self):
        '''Create a form fieldset from a model'''
        from pybald.core.forms import FieldSet
        from tests.sample_project.sample import SampleModel
        fs = FieldSet(SampleModel)
        assert fs.render().__html__() == expected_sample_fieldset

    def test_bind_data_to_form_and_save(self):
        '''Create a new model from a form'''
        from pybald.core.forms import FieldSet
        from tests.sample_project.sample import SampleModel
        fs = FieldSet(SampleModel, data={'SampleModel--text': 'this is totally a test'})
        if fs.validate():
            fs.sync()
        fs.model.save().commit()

    def test_edit_a_model(self):
        '''Edit an existing model by rebinding a form / fieldset'''
        from pybald.core.forms import FieldSet
        from pybald.core.forms import validators
        from tests.sample_project.sample import SampleModel
        sm = SampleModel(text="This is just some sample text already in the model.")
        sm.save().commit()
        fs = FieldSet(sm, data={'SampleModel-1-text': 'this is totally a test'})
        def text_only(value, field):
            if not (isinstance(value, str)):
                raise validators.ValidationError('Value must be text')
        assert fs.text.value == 'this is totally a test'
        fs.configure(options=[fs.text.validate(text_only)])
        if fs.validate():
            fs.sync()
            fs.model.commit()
        saved_sample = SampleModel.get(id=1)
        assert saved_sample.text == 'this is totally a test'

    def test_validation(self):
        '''Don't save a model with text value in a numeric validated field'''
        from pybald.core.forms import FieldSet
        from pybald.core.forms import validators
        from tests.sample_project.sample import SampleModel
        def number_only(value, field):
            if not (isinstance(value, int)):
                raise validators.ValidationError('Value must be a number')
        fs = FieldSet(SampleModel, data={'SampleModel--text': 'this is totally a test'})
        fs.configure(options=[fs.text.validate(number_only)])
        if fs.validate():
            fs.sync()
            fs.model.save().commit()
            self.fail("Model should not have validated")
