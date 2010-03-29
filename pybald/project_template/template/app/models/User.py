#!/usr/bin/env python
# encoding: utf-8
"""
User.py

Created by mikepk on 2009-07-07.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest
import app
from pybald.core.storage_engines.StoredObject import StoredObject

class User(StoredObject):
    # These three class variables must be defined, they determine how the object
    # maps to the stored object
    table = "users"
    key = "user_id"
    table_map = ['user_id',
                'username',
                'password',
                'main_card_id',
                'date_modified',
                'date_created',
                'status',
                'email']

    
    def __init__(self):
        StoredObject.__init__(self)
        self.user_id = None
        self.username = None
        self.email = None
        self.password = None
        self.status = None
        self.main_card_id = None


    def save(self):
        '''Save a user object into the store.'''
        # make sure the username is populated (being unique)
        if not self.username and self.email:
            self.username = self.email
        StoredObject.save(self)
        self._new = False

    def checkCredentials(self,email,password):
        '''Check login credentials.'''
        try:
            # TODO: this password needs to be SHA1 hashed
            self.load(email=email,password=password)
            return self
        except:
            return None

class UserTests(unittest.TestCase):
    def setUp(self):
        pass

    def testCreate(self):
        '''Try creating a user.'''
        user = User()
        user.username = "test user"
        user.user_id = 3
        user.status = 'OK'
        user.save()
        user2 = User()
        user2.username = "test user2"
        user2.user_id = 4
        user2.status = 'OK'
        user2.save()
        


if __name__ == '__main__':
	unittest.main()