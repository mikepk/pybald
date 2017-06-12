import unittest
from mako.template import Template
import pybald
from pybald import context
from datetime import datetime, timedelta
from pybald.core.router import Router


helpers = (
('page_js', '''${page.add_js('/test.js')}''', b'''<script src="/test.js?v=None"></script>''', {}),
('page_css', '''${page.add_css('/sample.css')}''', b'''<link type="text/css" href="/sample.css?v=None" media="screen" rel="stylesheet">''', {}),
('date_humanize_moment_ago', '''${humanize(moment_ago)}''', b'just a moment ago', {'moment_ago': (datetime.now() - timedelta(seconds=55)).strftime("%Y-%m-%d %H:%M:%S")}),
('date_humanize_hour', '''${humanize(an_hour_ago)}''', b'1 hour ago', {'an_hour_ago': (datetime.now() - timedelta(minutes=65)).strftime("%Y-%m-%d %H:%M:%S")}),
('date_humanize_minutes', '''${humanize(minutes_ago)}''', b'15 minutes ago', {'minutes_ago': (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")}),
('date_humanize_one_minute', '''${humanize(minute_ago)}''', b'1 minute ago', {'minute_ago': (datetime.now() - timedelta(seconds=68)).strftime("%Y-%m-%d %H:%M:%S")}),
('date_humanize_day', '''${humanize(a_day_ago)}''', b'1 day ago', {'a_day_ago': (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")}),
('date_humanize_future', '''${humanize(in_the_future)}''', b'in the future', {'in_the_future': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")}),
('date_humanize_multi_weeks', '''${humanize(multi_weeks_ago)}''', b'2 weeks ago', {'multi_weeks_ago': (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")}),
('date_humanize_more_than_30_days', '''${humanize(months_ago)}''', b'30 Mar', {'months_ago': (datetime.strptime('2017-05-14 15:00:27', "%Y-%m-%d %H:%M:%S") - timedelta(days=45)).strftime("%Y-%m-%d %H:%M:%S")}),
('date_humanize_more_than_1_year', '''${humanize(years_ago)}''', b'19 Apr &#39;16', {'years_ago': (datetime.strptime('2017-05-14 15:00:27', "%Y-%m-%d %H:%M:%S") - timedelta(days=390)).strftime("%Y-%m-%d %H:%M:%S")}),
('date_humanize_bad_input', '''${humanize(bad_format)}''', b'Jan 1st 2045', {'bad_format': 'Jan 1st 2045'}),
('generate_link', '''${link('A test link').to('home')}''', b'<a href="/" >A test link</a>', {}),
('generate_raw_link', '''${link('A test link').to_raw_url('http://pybald.com')}''', b'<a href="http://pybald.com" >A test link</a>', {}),
('create_image', '''${img('/sample.jpg')}''', b'<img src="/sample.jpg" alt="/sample.jpg" />', {}),
('html_literal', '''${literal('<h2>This is a literal html h2</h2>')}''', b'<h2>This is a literal html h2</h2>', {}),
('html_escaping', '''${'<h2>This h2 tag should be escaped</h2>'}''', b'&lt;h2&gt;This h2 tag should be escaped&lt;/h2&gt;', {}),
('plural_more', '''dog${plural(['spot', 'fido'])}''', b'dogs', {}),
('plural_single', '''dog${plural(['spot'])}''', b'dog', {}),
('as_p', '''${as_p(text_with_line_breaks)}''', b'<p>This is just</p><p>A test</p><p>of paragraph breaks</p>', {"text_with_line_breaks": "This is just\nA test\nof paragraph breaks"}),
('anchor_no_name', '''${anchor('a block')}''', b'<a name="a block" >a block</a>', {}),
('anchor_name', '''${anchor('a block', 'heading1')}''', b'<a name="heading1" >a block</a>', {}),
)


class TestTemplate(unittest.TestCase):
    def setUp(self):
        context = pybald.configure(config_file="tests/sample_project/project.py")

        def map(urls):
            urls.connect("home", r"/")

        self.app = Router(routes=map, controllers=[])

    def tearDown(self):
        context._reset()

    def test_template_lookup(self):
        '''Look up a template in the filesystem'''
        template = context.render._get_template('sample')
        # we've got a compiled template
        assert isinstance(template, Template)

    def test_template_render_with_data(self):
        '''Render a template with data.'''
        template = context.render._get_template('sample')
        assert template.render(sample_variable='sample') == b"<h1>Hello sample!</h1>"


def create_case(template, expected, data):
    def run_helper(self):
        result = context.render.raw_template(template, data)
        self.assertEqual(expected, result)
    return run_helper


def make_cases():
    for name, template, expected, data in helpers:
        test_method = create_case(template, expected, data)
        test_method.__name__ = 'test_template_helper_{}'.format(name)
        setattr(TestTemplate, test_method.__name__, test_method)

make_cases()