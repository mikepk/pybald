import unittest
import pybald
from pybald import context
from six import StringIO
from pybald.config import constants

test_constants = StringIO('''
[copyright]
year: 2017

[marketing]
burgers_served: billions and billions

[other]
phone: 555 555 1234
''')


class TestConstants(unittest.TestCase):
    def setUp(self):
        # rewind the constants file each time
        test_constants.seek(0)
        constants_values = constants.read(constants_file=test_constants)
        context = pybald.configure(page_options={'constants': constants_values})

    def tearDown(self):
        context._reset()

    def test_constant_copyright(self):
        self.assertEqual(context.render.raw_template(b'${constants.copyright.year}'), b'2017')

    def test_constant_marketing(self):
        print(context.config)
        self.assertEqual(context.render.raw_template(b'${constants.marketing.burgers_served}'), b'billions and billions')

    def test_constant_other(self):
        self.assertEqual(context.render.raw_template(b'${constants.other.phone}'), b'555 555 1234')
