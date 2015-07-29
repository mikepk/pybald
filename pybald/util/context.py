from threading import local
import logging
log = logging.getLogger(__name__)


class Proxy(object):
    '''A convenience proxy.'''
    def __init__(self, proxied_object):
        self._proxied_object = proxied_object

    def _proxied(self):
        return self._proxied_object

    def __dir__(self):
        return sorted(dir(self.__class__) + self.__dict__.keys() + dir(self._proxied()))

    def __getattr__(self, attr):
        return getattr(self._proxied(), attr)

    def __setattr__(self, attr, value):
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


class AppAttributeProxy(Proxy):
    def __init__(self, parent, attribute):
        self.parent = parent
        self.attribute = attribute

    def _proxied(self):
        return getattr(self.parent._proxied(), self.attribute)

    def __setattr__(self, attr, value):
        if attr in ('parent', 'attribute', '_proxied'):
            object.__setattr__(self, attr, value)
        else:
            super(AppAttributeProxy, self).__setattr__(attr, value)

    def __getattr__(self, attr):
        if attr in ('parent', 'attribute', '_proxied'):
            return object.__getattribute__(self, attr)
        else:
            return getattr(self._proxied(), attr)


class AppContext(Proxy):
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

    def __getattr__(self, attr):
        # return getattr(self._proxied(), attr)
        return AppAttributeProxy(self, attr)

