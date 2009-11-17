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
    
    # logins, on a post run process_login, otherwise display form
    rmap.connect('login/', controller='login', conditions=dict(method=['GET', 'HEAD']))
    rmap.connect('login/', controller='login', action='process_login', conditions=dict(method=['POST']))

    # logins, on a post run process_login, otherwise display form
    rmap.connect('register/', controller='register', conditions=dict(method=['GET', 'HEAD']))
    rmap.connect('register/', controller='register', action='process_registration', conditions=dict(method=['POST']))

    #info
    rmap.connect('what','what*(format)',controller='info',action='what')
    rmap.connect('how','how*(format)',controller='info',action='how')
    rmap.connect('getting_started','getting_started*(format)',controller='info',action='getting_started')

    
    # home
    rmap.connect('home','', controller='home')
    rmap.connect('index/:action', controller='home')    

    # cards RESTful mapping
    # rmap.resource('card', 'cards')
    # rmap.connect('cards/:id/photo', controller='cards', action='photo')

    # PUT doesn't work from browser
    # rmap.connect('cards/:id', controller='cards', action='update',
    #     conditions=dict(method=['POST']))


    # generic pattern
    rmap.connect(':controller/:action/:id')
