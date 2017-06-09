import unittest
import pybald
from pybald import context
from pybald.util.console import Console


test_config = dict(env_name="ConsoleTest",
                   config_object=True,
                   sample_config=True,
                   cache_path=None,
                   project_name="Console Testing",
                   debug=True,
                   template_helpers=['from pybald.core import assets'],
                   path="",
                   database_engine_uri='')


class TestConsole(unittest.TestCase):
    def setUp(self):
        pybald.configure(config_object=test_config)

    def tearDown(self):
        context._reset()

    def test_create_console(self):
        '''Create a pybald console'''
        try:
            console = Console(project_name=pybald.context.config.project_name or pybald.context.name,
                      app=None, additional_symbols=[])
        except Exception as err:
            self.fail(err)
