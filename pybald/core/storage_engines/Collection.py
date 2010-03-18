#!/usr/bin/env python
# encoding: utf-8
"""
Collection.py

Created by mikepk on 2009-08-15.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

from pybald.core.storage_engines.DbStore import DbStore


class Collection:
    def __init__(self):
        self.store = DbStore()
        self.orders = []
        self.limit_count = ''

    def load(self,obj_class,**where):
        options = self.parse_options()
        data = self.store.load_many(obj_class.table, where, options)
        if not data:
            return []
        
        collection = []
        for item in data:
            obj = obj_class()
            obj.create(item)
            obj._new = False
            collection.append(obj)

        return collection

    def load_join(self,obj_class,obj2_class,**where):
        options = self.parse_options()
        # data = self.store.load_many([obj_class.table,obj2_class.table], join_where, where, options)
        
        # TODO: make a JOIN object in the db model. THis is total HAck-Nastyness
        where_list = []
        for key in where.keys():
            where_list.append('''%s=%s''' % (key,where[key]))
        where_clause = "WHERE "+' AND '.join(where_list)
        statement = '''SELECT %s.* FROM %s JOIN %s %s %s''' % (obj_class.table, obj_class.table, obj2_class.table, where_clause, options)

        data = self.store.raw(statement,[])
        if not data:
            return []
        
        collection = []
        for item in data:
            obj = obj_class()
            obj.create(item)
            obj._new = False
            collection.append(obj)

        return collection
        

    def parse_options(self):
        option = ''
        if self.orders:
            option += ' ORDER BY '+', '.join(self.orders)
        if self.limit_count:
            option += ' LIMIT '+str(self.limit_count)
        return option
    
    def order_by(self,member,direction=None):
        if direction:
            self.orders.append(str(member)+' '+str(direction))
        else:
            self.orders.append(str(member))
        return self
    
    def limit(self,count):
        self.limit_count = count
        return self


class CollectionTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()