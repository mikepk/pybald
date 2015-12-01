import unittest

class TestEngine(unittest.TestCase):
    def setUp(self):
        pass

    def test_unconfigured_engine(self):
        "Raise an exception when the db engine is not configured"
        try:
            from pybald.context import models
            models.engine.execute("SELECT 1234")
        except RuntimeError as err:
            pass
        else:
            self.fail('Runtime exception not thrown')