from threading import local
import logging
log = logging.getLogger(__name__)

class AppAttributeProxy(object):
    def __init__(self, app):
        self.app = app

    def __getattr__(self, attr):
        print "inside", attr
        # return self._proxied()
        print type(self.app._proxied())
        # print type(getattr(self.app, attr))
        return getattr(getattr(self.app._proxied(), attr), attr)

class AppContext(object):
    '''A convenience proxy that represents the configured application.

    Stores data in a simple thread local on a stacked list.'''
    def __init__(self, *pargs, **kargs):
        self.__dict__['___threadlocal__'] = local()
        self.__dict__['___threadlocal__'].stack = []
        self.__dict__['___stack__'] = self.__dict__['___threadlocal__'].stack

    def _set_proxy(self, obj):
        self.__dict__['___stack__'].append(obj)

    def _pop_proxy(self):
        return self.__dict__['___stack__'].pop()

    def _proxied(self):
        try:
            return self.__dict__['___stack__'][-1]
        except IndexError:
            raise RuntimeError("No Pybald application is configured.")

    def __dir__(self):
        return sorted(dir(self.__class__) + self.__dict__.keys() + dir(self._proxied()))

    def __getattr__(self, attr):
        return getattr(self._proxied(), attr)

    def __setattr__(self, attr, value):
        log.debug(attr)
        setattr(self._proxied(), attr, value)

    def __delattr__(self, attr):
        delattr(self._proxied(), attr)

    def __getitem__(self, key):
        return self._proxied()[key]

    def __setitem__(self, key, value):
        self._proxied()[key] = value

    def __delitem__(self, key):
        del self._proxied()[key]

    def __call__(self, *args, **kw):
        return self._proxied()(*args, **kw)

    def __repr__(self):
        try:
            return repr(self._proxied())
        except (TypeError, AttributeError):
            return str(self)

    def __iter__(self):
        return iter(self._proxied())

    def __len__(self):
        return len(self._proxied())

    def __contains__(self, key):
        return key in self._proxied()

    def __nonzero__(self):
        return bool(self._proxied())

