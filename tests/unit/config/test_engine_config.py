import unittest

class TestEngine(unittest.TestCase):
    def setUp(self):
        pass

    def test_unconfigured_engine(self):
        "Raise an exception when the db engine is not configured"
        from pybald.context import engine
        try:
            engine.execute("SELECT 1234")
        except RuntimeError:
            pass
        else:
            self.fail('Runtime exception not thrown')