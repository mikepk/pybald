import sys
class ConfigWrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
    def __getattr__(self, name):
        # Some sensible default?
        return getattr(self.wrapped, name, None)
    def __dir__(self):
        return dir(self.wrapped)

controllers_module = '.'
database_engine_args = {}
sys.modules[__name__] = ConfigWrapper(sys.modules[__name__])
