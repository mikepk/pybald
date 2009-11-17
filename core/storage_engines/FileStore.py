#!/usr/bin/env python
# encoding: utf-8
"""
FileStore.py

Created by mikepk on 2009-07-06.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

import pickle
import app


class FileStore:
    def __init__(self):
        self.file_store_path = '/var/tmp/filestore'

    def set_file_path(self,path):
        self.file_store_path = path

    def save(self,obj):
        '''Save object to the filesystem.'''
        file_path = self.get_file_path(obj.__class__.table,obj.__class__.key,obj[obj.__class__.key])
        obj_file = open(file_path,'w')
        pickle.dump(obj,obj_file)
        obj_file.close()
        return 1
        
    def load(self,obj): #table,keyname,key):
        '''Load object from the filesystem.'''
        file_path = self.get_file_path(obj.__class__.table,obj.__class__.key,obj[obj.__class__.key])
        obj_file = open(file_path,'r')
        data = pickle.load(obj_file)
        obj_file.close()
        return data
    
    def delete(self,obj):
        '''Delete object from the filesystem.'''
        pass

    def get_file_path(self,table,keyname,key):
        '''Create the path for an object in the filestore dir.'''
        table_path = os.path.join(self.file_store_path,table)
        # check the table, no? create
        if not os.path.exists(table_path):
            os.mkdir(table_path) 
        return os.path.join(table_path,keyname+'_'+str(key))
        
    def sync(self,obj,table):
        '''Filestore does not do anything special to sync stored data with object.'''
        pass


class FileStoreTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()