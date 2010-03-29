#!/usr/bin/env python
# encoding: utf-8
"""
Session.py

Created by mikepk on 2009-07-06.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

import hashlib
import random

import pickle

import zlib

from pybald.core.storage_engines.StoredObject import StoredObject
from pybald.core.storage_engines.StoredObject import NotFound
from app.models.User import User

class Session(StoredObject):
    '''A session object for tracking users throughtout the system.'''
    table = "sessions"
    key = "session_id"
    table_map = ['session_id',
                'user_id',
                'cache']

    def __init__(self):
        StoredObject.__init__(self)
        self.user = None
        self.session_id = None
        self.cachestore = {}
        self.cache = ''
        
    def generate_id(self):
        '''Generate a session_id key for the session'''
        if not self.__dict__[self.__class__.key]:
            # user current time as seed
            random.seed()
            # choose a random num up to 2^32
            key = random.randint(1,2**32)
            # hash it for a unique session_id
            self.__dict__[self.__class__.key] = hashlib.sha1('SALT SALT SALT SALT'+str(key)).hexdigest()
        self.session_id = self.__dict__[self.__class__.key]

    def set_user(self,user):
        self.user = user
        self.user_id = user.user_id
        return 1

    def create_session(self):
        pass
    
    def save(self):
        '''Save a session to the database, including the small session cache.'''
        #self.cache = zlib.compress(pickle.dumps(self.cachestore))
        self.cache = pickle.dumps(self.cachestore)
        print "CACHE LENGTH: "+str(len(self.cache))
        #print str(len(self.cache))
        #print "Compressed "+str(len(zlib.compress(self.cache)))
        StoredObject.save(self)


    def load(self,session_id=None):
        try:
            session = StoredObject.load(self,session_id)
        except NotFound:
            raise

        if session.cache:
            try:
                #session.cachestore = pickle.loads(zlib.decompress(session.cache))
                session.cachestore = pickle.loads(session.cache)
                #print "SESSION CACHE "+str(len(str(session.cachestore))) #+str(session.cachestore)
            except:
                raise # TypeError, 'Cache load fail.'

        # 
        # if session.user_id:
        #     try:
        #         session.user = User().load(session.user_id)
        #     except NotFound:
        #         session.user = None
        #         session.user_id = None
        #         session.save()
        return session


class SessionTests(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()