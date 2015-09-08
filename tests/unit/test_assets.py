import unittest

sample_with_bundles = '''
<bundle filters="cssmin">
<link type="text/css" href="/css/test1.css" media="screen" rel="stylesheet">
<link type="text/css" href="/css/test2.css" media="screen" rel="stylesheet">
</bundle>
<bundle filters="rjsmin">
<script src="/js/test1.js"></script>
<script src="/js/test2.js"></script>
</bundle>
'''

test_config=dict(sample_config=True,
                env_name="SampleTestProjectEnvironment",
                template_path="tests/sample_project/",
                cache_path=None,
                project_name="Sample Project",
                debug=True,
                template_helpers=['from pybald.core import assets'],
                BUNDLE_SOURCE_PATHS=['tests/sample_project/public',
                                     'tests/sample_project/sass'],
                BUNDLE_ASSETS=True,
                # BUNDLE_OUTPUT_PATH='tests/sample_project/public/min',
                # BUNDLE_MANIFEST='tests/sample_project/tmp/webasset_manifest',
                path="",
                static_path="tests/sample_project/public",
                database_engine_uri='sqlite:///:memory:')

class TestWebassets(unittest.TestCase):
    def setUp(self):
        pass
        # import pybald
        # context = pybald.configure(config_object=test_config)
        # print(context.config)
        # from pybald.core.assets import Bundler
        # b = Bundler()
        # self.bundle = b.bundle
        # print(context.config)

    # def test_bundles(self):
    #     '''Run webasset bundling'''
    #     # from pybald import context
    #     data = sample_with_bundles
    #     print(self.bundle(data))
    #     # print(data)
    #     assert False

