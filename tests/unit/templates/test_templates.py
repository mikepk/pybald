import unittest
from mako.template import Template

class TestTemplate(unittest.TestCase):
    def setUp(self):
        import pybald
        context = pybald.configure(config_file="tests/sample_project/project.py")
        from tests.sample_project.sample import app

    def test_template_lookup(self):
        from pybald import context
        template = context.render._get_template('sample')
        # we've got a compiled template
        assert isinstance(template, Template)

    def test_template_render_with_data(self):
        from pybald import context
        template = context.render._get_template('sample')
        assert template.render(sample_variable='sample') == "<h1>Hello sample!</h1>"

    def test_template_with_helpers(self):
        from pybald import context
        from datetime import datetime, timedelta
        a_day_ago = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        an_hour_ago = (datetime.now() - timedelta(minutes=65)).strftime("%Y-%m-%d %H:%M:%S")
        rendered_template = context.render('sample_with_helpers',
                             dict(sample_variable='sample',
                             an_hour_ago=an_hour_ago,
                             a_day_ago=a_day_ago))
        expected_result = '''page javascript:
    <script src="/test.js?v=None"></script>
    <link type="text/css" href="/sample.css?v=None" media="screen" rel="stylesheet">
humanized dates:
    1 hour ago
    1 day ago
link, img helpers:
    <a href="A test link" >home</a>
    <img src="/sample.jpg" alt="/sample.jpg" />
test default filters:
    <h2>This is a literal html h2</h2>
    &lt;h2&gt;This h2 tag should be escaped&lt;/h2&gt;
'''
        print(rendered_template)
        assert rendered_template == expected_result

