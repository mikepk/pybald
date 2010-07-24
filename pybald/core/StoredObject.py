#!/usr/bin/env python
# encoding: utf-8
"""
StoredObject.py

Created by mikepk on 2010-04-21.
Copyright (c) 2010 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

import project
from sqlalchemy.orm import reconstructor

from app.models import DbSession as db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

class StoredObject:
    '''Generic StoredObject all models inherit from.'''
    NoResultFound = NoResultFound
    MultipleResultsFound = MultipleResultsFound

    def __init__(self):
        self.__db_init__()
    
    @reconstructor
    def __orm_init__(self):
        '''Called when objects are loaded from db by sqlalchemy. Initializes non db and transient values.'''
        self.__db_init__()

    def __db_init__(self):
        self.db_session = db

    
    def save(self,commit=False):
        '''Save this instance. When commit is False, stages data for later commit.'''
        # if not self.session:
        #     self.session = Session()
        db.add(self)
        
        if commit:
            self.commit()
        return self

    def commit(self):
        '''Call the commit for the entire session (includes anything else pending)'''
        # if not self.session:
        #     self.session = Session()
        db.commit()
        # self.session.commit()


    @classmethod
    def load(cls,**where):
        '''Builds a sqlalchemy load query to return stored objects. Must execute the query to retrieve.'''
        # session = Session()
        return db.query(cls).filter_by(**where)

    @classmethod
    def query(cls):
        return db.query(cls)

    @classmethod
    def load_list(cls,arg):
        return db.query(cls).filter(arg)
        

    class NotFound(Exception):
        pass

class StoredObjectTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()