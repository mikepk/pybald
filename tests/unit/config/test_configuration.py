import unittest
import pybald
from pybald import context

class TestConfig(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        context._reset()

    def test_default_config(self):
        "Start without a config, a default configuration is used"
        context = pybald.configure()
        assert context.config.debug == True
        assert context.config.env_name == 'Default'

    def test_read_from_file(self):
        "Read a pybald config from a file"
        context = pybald.configure(config_file="tests/sample_project/project.py")
        assert context.config.sample_config == True
        assert context.config.env_name == 'SampleTestProjectEnvironment'

    def test_read_from_object(self):
        "Pass pybald configuration as a dictionary of values"
        config_obj = dict(conf_object=True, env_name="TestFromObject")
        context = pybald.configure(config_object=config_obj)
        assert context.config.conf_object == True
        assert context.config.env_name == "TestFromObject"

    def test_missing_file(self):
        "Exit if specified config file is missing"
        with self.assertRaises(SystemExit) as context:
            pybald.configure(config_file="tests/sample_project/not_there.py")
