#!/usr/bin/env python
# encoding: utf-8
"""
project.py

A module to hold project specific members and configuration.

Created by mikepk on 2009-07-24.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

path = ''

# define project routes for the URL mapper
def set_routes(rmap):
    '''Simple function to define routes. A routes map object should be passed in.'''

    # the order of the routes is important, more specific should come before
    # more generic
    
    # home
    rmap.connect('home','', controller='home')
    rmap.connect('index/{action}', controller='home')    

    # cards RESTful mapping
    # rmap.resource('card', 'cards')

    # generic pattern
    rmap.connect('{controller}/{action}/{id}')
