#!/usr/bin/env python
# encoding: utf-8
"""
DbStore.py

Created by mikepk on 2009-07-26.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

import pickle

import app
import project

from pybald.core.pyboxdb.pyboxdb import pdb
#Pyboxdb
import re

class DbStore:
    def __init__(self):
        #pdb = Pyboxdb()
        pdb.set_connection_string(project.get_db_connection_string())
        self.connect()

    def connect(self):
        pdb.connect()
        
    def save(self,table,data):
        '''Save object to a db.'''
        pdb.sqlInsert(table,data)
        return 1
        
    def update(self,table,key,value,data):
        '''Update an existing record.'''
        pdb.sqlUpdate(table,data,{key:value})
        return 1

    def load(self,table,where): #key,value):
        '''Load object from a db.'''
        data = pdb.sqlSelect('*',table,where) 
        return data

    def load_many(self,table,where,opt):
        '''Load ordered collection of objects from a db.'''
        if isinstance(table,list):
            select = table[0]+'.*'
        else:
            select = '*'
            
        data = pdb.sqlSelect(select,table,where,opt)
        return data

    def delete(self,table,where):
        '''Delete object from the filesystem.'''
        pdb.sqlDelete(table,where)
        return 1

    def getLastId(self):
        '''Get last insert ID.'''
        return pdb.sqlLastInsertId()

    def get_file_path(self,table,keyname,key):
        '''Create the path for an object in the filestore dir.'''
        table_path = os.path.join(file_store_path,table)
        # check the table, no? create
        if not os.path.exists(table_path):
            os.mkdir(table_path) 
        return os.path.join(table_path,keyname+'_'+str(key))

    def sync(self,obj,table):
        '''dbstore does not do anything special to sync stored data with object.'''
        pass

    def raw(self,statement,values=None):
        '''Pass raw SQL.'''
        return pdb.sqlRaw(statement,values)

class DbStoreTests(unittest.TestCase):
    def setUp(self):
        self.dbstore = DbStore()

    def testSave(self):
        from app.models.User import User
        ed = User()
        ed.username = "Edwardo2"
        ed.email = "ed@ed.com"
        self.dbstore.save(ed)

if __name__ == '__main__':
    unittest.main()