import unittest
from mako.template import Template

class TestWebassets(unittest.TestCase):
    def setUp(self):
        import pybald
        context = pybald.configure(config_file="tests/sample_project/project.py")
        from tests.sample_project.sample import app

    # def test_bundles(self):
    #     '''Run webasset bundling'''
    #     from pybald import context
    #     template = context.render._get_template('sample_with_bundles')
    #     data = template.render()
    #     print(data)
    #     assert False
    #     # we've got a compiled template
    #     # assert isinstance(template, Template)

