import unittest

class TestEngine(unittest.TestCase):
    def setUp(self):
        pass

    # def test_nothing(self):
    @unittest.skip("unconfigured exceptions not working in Py3")
    def test_unconfigured_engine(self):
        "Raise an exception when the db engine is not configured"
        with self.assertRaises(RuntimeError) as context:
            from pybald.context import models
            models.engine.execute("SELECT 1234")
        # except RuntimeError as err:
        #     pass
        # else:
        #     self.fail('Runtime exception not thrown')