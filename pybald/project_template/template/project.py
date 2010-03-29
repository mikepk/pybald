#!/usr/bin/env python
# encoding: utf-8
"""
project.py

A module to hold project specific members and configuration.

Created by mikepk on 2009-07-24.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""
import os
import re

path = ''



def get_db_connection_string():
    '''Get the database credentials for connection.'''
    return {'host':'localhost', 'user':'dbuser', 'passwd':'dbpwd', 'db':'dbname'}

# define project routes for the URL mapper
def set_routes(rmap):
    '''Simple function to define routes. A routes map object should be passed in.'''

    # the order of the routes is important, more specific should come before
    # more generic
    
    # logins, on a post run process_login, otherwise display form
    # rmap.connect('login/', controller='login', conditions=dict(method=['GET', 'HEAD']))
    # rmap.connect('login/', controller='login', action='process_login', conditions=dict(method=['POST']))

    # home
    rmap.connect('home','', controller='home')
    rmap.connect('index/{action}', controller='home')    

    # RESTful mapping
    # rmap.resource('card', 'cards')

    # generic pattern
    rmap.connect('{controller}/{action}/{id}')

def get_path():
    '''Return the project path.'''
    return os.path.dirname( os.path.realpath( __file__ ) )
