#!/usr/bin/env python
# encoding: utf-8
"""
StoredObject.py

Created by mikepk on 2009-07-05.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

from pybald.core.storage_engines.DbStore import DbStore

# change this line to switch the storage type
# can be FileStore, DBStore, possibly Google store
# in the future
store = DbStore()

class NotFound(Exception):
    pass

class StoredObject:
    '''A generic stored object superclass. This object defines methods for save, load, delete and update. (Basic CRUD).'''
    NotFound = NotFound
    IntegrityError = DbStore.IntegrityError
    def __init__(self,key=None,table=None):
        self._new = True

    def load(self,keyvalue=None,**otherwhere):
        '''Load a single object from the store.'''        

        if otherwhere:
            where = otherwhere
        else:
            where = {}

        # check whether the object has a key already, if one is passed in, assign it to the object
        if not self.__dict__[self.__class__.key] and keyvalue:
            self.__dict__[self.__class__.key] = keyvalue
            where[self.__class__.key] = self.__dict__[self.__class__.key];

        # Check the object if it has a primary id key or a where clause to search
        if not self.__dict__[self.__class__.key] and not otherwhere:
            raise TypeError, "If Stored object doesn't have a primary key value, one must be provided."

        data = store.load(self.__class__.table, where)
        if not data:
            raise NotFound, "Item not found."

        # the create method populates the object
        # with the data from the store. For 'load'
        # it just uses the first row returned (if multi)
        self.create(data[0])
        return self

    def create(self,data):
        '''Populate the item members from the data.'''
        for key in data:
            self[key] = data[key]
        # loaded so not new
        self._new = False
        return 1
        
        
    def update(self):
        '''Update an object in the store.'''
        data = {}
        for key in self.__class__.table_map:
            # print '''key %s value %s''' % (key, data[key])
            if key == 'date_created':
                # special case, date created requires a null insertion
                # to populate due to weird mysql implementation. So if we don't
                # have one in the data structure, we're somehow new, so force NULL
                try:
                    if self[key]:
                        pass
                # no created date? Is it a new object? Set to none.
                except KeyError:
                    data[key] = None
            elif key == 'date_modified':                
                # special case, date modified shouldn't be echoed
                # back to the server (so it can reflect update changes)
                pass
            # elif self[key] == 0 or self[key]:
            #     data[key] = self[key]
            else:
                data[key] = self[key]

        store.update(self.__class__.table, self.__class__.key, self.__dict__[self.__class__.key], data)
        return self


    def save(self):
        '''Save a *new* object in the store. Updates are processed with update.'''
        # If this object does not have the new flag set update, otherwise save
        if not self._new:
            return self.update()

        data = {}
        # use the table map to build the object for saving
        for key in self.__class__.table_map:
            # special case, NULL must be inserted into date_created to get it
            # to set properly in MySQL (TODO: Move this to DBStore)
            if key=='date_created':
                data['date_created'] = None
            if self[key]:
                data[key] = self[key]
        
        store.save(self.__class__.table, data)
        if not self.__dict__[self.__class__.key]:
            self.__dict__[self.__class__.key] = store.getLastId()

        #once we've saved, we now update
        self._new = False
        return self
    
    def delete(self,**otherwhere):
        '''delete an object in the store'''
        where = {}
        where[self.__class__.key] = self.__dict__[self.__class__.key]
        return store.delete(self.__class__.table, where)
    
    def __iter__(self):
        '''Make stored objects iterable.'''
        for item in self.__dict__:
            yield item
            
    def __getitem__(self,key):
        '''Implement object as dictionary, getitem.'''
        try:
            return self.__dict__[key]
        except KeyError:
            return None

    def __setitem__(self,key,value=None):
        '''Implement object as dictionary, setitem.'''
        self.__dict__[key] = value
        return value
        
class StoredObjectTests(unittest.TestCase):
    def setUp(self):
        pass
            
    def testsave(self):
        '''Test Object Store Save'''
        so = StoredObject()
        so._key = "test"
        so._table = "test"
        self.assert_(so.save())
        
    def testload(self):
        '''Test Object Store Load'''
        import random

        so = StoredObject("testload","test")
        # generate some pseudo random data to compare save vs load
        so.data = random.randrange(0,4096,1)
        so.save()

        lo = StoredObject(table="test")
        lo = lo.load("testload")
        self.assert_(lo.data == so.data)

if __name__ == '__main__':
    unittest.main()