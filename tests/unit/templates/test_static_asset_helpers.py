import unittest
import pybald
from pybald import context
from pybald.core.helpers import AssetUrl
from routes import request_config


test_config = dict(STATIC_SOURCES=["example_cdn.com", "pybald.com"],
                   STATIC_HOSTS=["s0.sample.com"],
                   CDN_HOST="awesomecdn.com",
                   DEFAULT_PROTOCOL="https")

my_static_resource = "/static_stuff.js"
my_static_resource_explicit = "http://example_cdn.com/static_stuff.js"
not_owned_static_resource = "https://bing.com/static_stuff.js"


class TestStaticAssets(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        if hasattr(request_config(), "protocol"):
            del request_config().protocol
        context._reset()

    def test_dont_cdn_relative_url_rewrite_when_off(self):
        '''No re-writing if CDN is off'''
        a_test_config = test_config.copy()
        a_test_config["USE_CDN"] = False
        pybald.configure(config_object=a_test_config)
        asset_url = AssetUrl(my_static_resource)
        self.assertEqual(str(asset_url), str(my_static_resource))

    def test_dont_cdn_absolute_url_rewrite_when_off(self):
        '''No re-writing if CDN is off'''
        a_test_config = test_config.copy()
        a_test_config["USE_CDN"] = False
        pybald.configure(config_object=a_test_config)
        asset_url = AssetUrl(my_static_resource_explicit)
        self.assertEqual(str(asset_url), str(my_static_resource_explicit))

    def test_cdn_relative_url_rewrite_http(self):
        '''Test that relative link gets changed to a CDN link'''
        request_config().protocol = "http"
        a_test_config = test_config.copy()
        a_test_config["USE_CDN"] = True
        pybald.configure(config_object=a_test_config)
        asset_url = AssetUrl(my_static_resource)
        self.assertEqual(str(asset_url), 'http://s0.sample.com/static_stuff.js')

    def test_cdn_absolute_url_rewrite_http(self):
        '''Test that an absolute link gets changed to a CDN link'''
        request_config().protocol = "http"
        a_test_config = test_config.copy()
        a_test_config["USE_CDN"] = True
        pybald.configure(config_object=a_test_config)
        asset_url = AssetUrl(my_static_resource_explicit)
        self.assertEqual(str(asset_url), 'http://s0.sample.com/static_stuff.js')

    def test_cdn_url_rewrite_https(self):
        '''Test that the CDN rewrite is smart enough to use the raw CDN if
        https and we don't have https certs for static hosts.'''
        request_config().protocol = "https"
        a_test_config = test_config.copy()
        a_test_config["USE_CDN"] = True
        pybald.configure(config_object=a_test_config)
        asset_url = AssetUrl(my_static_resource)
        self.assertEqual(str(asset_url), 'https://awesomecdn.com/static_stuff.js')

    def test_dont_cdn_url_rewrite_for_unowned_link(self):
        '''Don't rewrite links on hosts we don't own'''
        request_config().protocol = "https"
        a_test_config = test_config.copy()
        a_test_config["USE_CDN"] = True
        pybald.configure(a_test_config)
        asset_url = AssetUrl(not_owned_static_resource)
        self.assertEqual(str(asset_url), str(not_owned_static_resource))

    def test_default_protocol(self):
        '''Test that the CDN rewrite is smart enough to use the raw CDN if
        https and we don't have https certs for static hosts.'''
        a_test_config = test_config.copy()
        a_test_config["USE_CDN"] = True
        pybald.configure(config_object=a_test_config)
        asset_url = AssetUrl(my_static_resource)
        self.assertEqual(str(asset_url), 'https://awesomecdn.com/static_stuff.js')