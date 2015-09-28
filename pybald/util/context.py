from threading import local
import logging
log = logging.getLogger(__name__)


class Proxy(object):
    '''A convenience proxy implementing most of the pass through methods.'''
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
        return repr(self._proxied())

    def __iter__(self):
        return iter(self._proxied())

    def __len__(self):
        return len(self._proxied())

    def __contains__(self, key):
        return key in self._proxied()

    def __bool__(self):
        return bool(self._proxied())

    def __nonzero__(self):
        return bool(self._proxied())

    def __add__(self, obj):
        return self._proxied().__add__(obj)

    def __radd__(self, obj):
        return self._proxied().__radd__(obj)

    @property
    def __class__(self):
        return self._proxied().__class__

    @property
    def __file__(self):
        return self._proxied().__file__


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
    '''A convenience proxy that represents the current active configured
    application.

    Stores data in a simple thread local on a stacked list.'''

    def __init__(self, *pargs, **kargs):
        self.__dict__['___threadlocal__'] = local()
        self.__dict__['___threadlocal__'].stack = []
        self.__dict__['___stack__'] = self.__dict__['___threadlocal__'].stack

    def _push(self, obj):
        self.__dict__['___stack__'].append(obj)

    def _pop(self):
        return self.__dict__['___stack__'].pop()

    def _proxied(self):
        try:
            return self.__dict__['___stack__'][-1]
        except IndexError:
            return None

    def __getattr__(self, attr):
        '''For all attributes of the wrapped object, return an AttributeProxy.

        This attribute proxy allows importing attributes and still maintaining
        the proxy behavior to look up the current context when accessing
        variables.

        This also allows late binding runtime configuration variables. This
        could be dangerous if a typo is introduced or other issue, the
        late code won't show an import error and instead will throw an
        attribute error when the late bound variable is accessed.
        '''
        return AppAttributeProxy(self, attr)

