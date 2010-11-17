#!/usr/bin/env python
# encoding: utf-8
"""
helpers.py

A set of HTML helpers for the templates. This includes link generating code, and special
escaping code.

Created by mikepk on 2009-07-08.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

#url_for takes these arguments as well
# anchor          specified the anchor name to be appened to the path
# host            overrides the default (current) host if provided
# protocol        overrides the default (current) protocol if provided
# qualified       creates the URL with the host/port information as 
#                 needed

# TODO: add javascript escape code here so it's available in the template engine

from routes import url_for

class Img_Object():
    def __init__(self,src=''):
        self.img_src = src
        self.attribs = []

    def __repr__(self):
        '''Return the link in string form.'''
        attr = " ".join(self.attribs) #[key,value for x in self.attribs])
        return '''<img src="%s" %s />''' % (self.img_src,attr)

    def set(self,**kargs):
        for key in kargs:
            akey = key.lstrip('_')
            self.attribs.append('''%s="%s"''' % (akey,kargs[key]))
        return self
    

class Link_Object():
    def __init__(self,link_text=''):
        self.link_text = link_text
        self.url = "#"
        self.attribs = []
    
    def to(self,*pargs,**kargs):
        self.url = url_for(*pargs,**kargs)
        return self
    
    def set(self,**kargs):
        for key in kargs:
            akey = key.lstrip('_')
            self.attribs.append('''%s="%s"''' % (akey,kargs[key]))
        return self
    
    def __repr__(self):
        '''Return the link in string form.'''
        attr = " ".join(self.attribs) #[key,value for x in self.attribs])
        return '''<a href="%s" %s>%s</a>''' % (self.url,attr,self.link_text)

def link(link_text='',img=None):
    lk = Link_Object(link_text)
    return lk

def img(src=None):
    if not src:
        return ''
    img = Img_Object(src)
    return img
