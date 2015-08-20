import unittest
import pybald
from pybald.core.controllers import Controller
from pybald.db.models import Model
from mako.template import Template

class TestTemplate(unittest.TestCase):
    def setUp(self):
        import pybald
        context = pybald.configure(config_file="tests/sample_project/project.py")
        from tests.sample_project.sample import app

    def test_template_lookup(self):
        from pybald import context
        template = context.render.lookup.get_template('sample.html.template')
        # we've got a compiled template
        assert isinstance(template, Template)

    def test_template_render_with_data(self):
        pass

    def test_template_with_helpers(self):
        pass
