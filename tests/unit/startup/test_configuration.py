import unittest
from collections import namedtuple
from nose.tools import eq_
import pybald

class TestConfig(unittest.TestCase):
    def setUp(self):
        pass

    def test_default_config(self):
        context = pybald.configure()
        eq_(context.config.debug, True)
        eq_(context.config.env_name, 'Default')

    def test_read_from_file(self):
        context = pybald.configure(config_file="tests/sample_project/project.py")
        eq_(context.config.sample_config, True)
        eq_(context.config.env_name, 'SampleTestProjectEnvironment')

    def test_read_from_object(self):
        config_obj = dict(conf_object=True, env_name="TestFromObject")
        context = pybald.configure(config_object=config_obj)
        eq_(context.config.conf_object, True)
        eq_(context.config.env_name, "TestFromObject")

