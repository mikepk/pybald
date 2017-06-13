import json
import pickle
import zlib

# from sqlalchemy.orm.interfaces import SessionExtension
from sqlalchemy.ext.mutable import Mutable

from sqlalchemy.types import (
    TypeDecorator,
    VARCHAR,
    PickleType
    )

# py3 compatibility
try:
    unicode
except NameError:
    unicode = str
from six import iteritems


class ASCII(TypeDecorator):
    '''
    A database string type that only allows ASCII characters.

    This is a data type check since all strings in the database could
    be unicode.
    '''
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        '''
        Run encode on a unicode string to make sure the string only
        contains ASCII characterset characters. To avoid another conversion
        pass, the original unicode value is passed to the underlying db.
        '''
        # run an encode on the value with ascii to see if it contains
        # non ascii. Ignore the return value because we only want to throw
        # an exception if the encode fails. The data can stay unicode for
        # insertion into the db.
        if value is not None:
            value.encode('ascii')
        return value

    def process_result_value(self, value, dialect):
        '''
        Run encode on a unicode string coming out of the database to turn the
        unicode string back into an encoded python bytestring.
        '''
        if isinstance(value, unicode):
            value = value.encode('ascii')
        return value


class JSONEncodedDict(TypeDecorator):
    '''
    Represents a dictionary as a json-encoded string in the database.
    '''
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        '''
        Turn a dictionary into a JSON encoded string on the way into
        the database.
        '''
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        '''
        Turn a JSON encoded string into a dictionary on the way out
        of the database.
        '''
        if value is not None:
            value = json.loads(value)
        return value


class ZipPickler(object):
    '''Simple wrapper for pickle that auto compresses/decompresses values'''
    def loads(self, string):
        return pickle.loads(zlib.decompress(string))

    def dumps(self, obj, protocol):
        return zlib.compress(pickle.dumps(obj, protocol))


class ZipPickleType(PickleType):
    def __init__(self, *pargs, **kargs):
        super(ZipPickleType, self).__init__(pickler=ZipPickler(), *pargs, **kargs)


class MutationDict(Mutable, dict):
    '''
    A dictionary that automatically emits change events for SQA
    change tracking.

    Lifted almost verbatim from the SQA docs.
    '''
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutationDict."
        if not isinstance(value, MutationDict):
            if isinstance(value, dict):
                return MutationDict(value)
            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def update(self, *args, **kwargs):
        '''
        Updates the current dictionary with kargs or a passed in dict.
        Calls the internal setitem for the update method to maintain
        mutation tracking.
        '''
        for k, v in iteritems(dict(*args, **kwargs)):
            self[k] = v

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."
        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."
        dict.__delitem__(self, key)
        self.changed()

    def __getstate__(self):
        '''Get state returns a plain dictionary for pickling purposes.'''
        return dict(self)

    def __setstate__(self, state):
        '''
        Set state assumes a plain dictionary and then re-constitutes a
        Mutable dict.
        '''
        self.update(state)

    def pop(self, *pargs, **kargs):
        """
        Wrap standard pop() to trigger self.changed()
        """
        result = super(MutationDict, self).pop(*pargs, **kargs)
        self.changed()
        return result

    def popitem(self, *pargs, **kargs):
        """
        Wrap standard popitem() to trigger self.changed()
        """
        result = super(MutationDict, self).popitem(*pargs, **kargs)
        self.changed()
        return result

__all__ = ['ASCII', 'JSONEncodedDict', 'ZipPickler', 'MutationDict', 'ZipPickleType']
