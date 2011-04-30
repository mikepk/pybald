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

from datetime import datetime
from routes import url_for
from mako import filters

static_prefix="http://static.smarterer.com"

class tag(object):
    def set(self,**kargs):
        for key in kargs:
            akey = key.rstrip('_')
            self.attribs.append('''%s="%s"''' % (akey,kargs[key]))
        return self
    

class img(tag):
    def __init__(self,src='', **kargs):
        self.img_src = src
        self.attribs = []
        self.set(**kargs)

    def __str__(self):
        '''Return the image in string form.'''
        image_url='''{0}{1}'''.format(static_prefix,self.img_src)
        if "alt" not in self.attribs:
            self.attribs.append('''alt="{0}"'''.format(image_url))
        attr = " ".join(self.attribs) #[key,value for x in self.attribs])
        return '''<img src="{0}" {1} />'''.format(image_url,attr)

    

class link(tag):
    def __init__(self,link_text='', **kargs):
        self.link_text = link_text
        self.url = "#"
        self.attribs = []
        self.set(**kargs)

    def filter(self, filter_type="h"):
        self.link_text = filters.html_escape(self.link_text)
        return self
    
    def to(self, *pargs, **kargs):
        self.url = url_for(*pargs, **kargs)
        return self
    
    def __str__(self):
        '''Return the link in string form.'''
        attr = " ".join(self.attribs) #[key,value for x in self.attribs])
        return '''<a href="%s" %s>%s</a>''' % (self.url,attr,self.link_text)

def plural(list_object):
    '''Return "s" for > 1 items'''
    if len(list_object) > 1:
        return "s"
    else:
        return ""
        

def humanize(date_string):
    format = "%Y-%m-%d %H:%M:%S"
    try:
        date = datetime.strptime(date_string, format)
    except:
        return date_string
    now = datetime.now()
    delta = now - date
    plural = 's'
    if delta.days >= 1:
        if delta.days == 1:
            plural = ''
        return "%s day%s ago" % (str(delta.days),plural)
    # > 1 hour, display in hours
    elif delta.seconds > 3600:
        hours = int(round(delta.seconds / 3600.0))
        if hours == 1:
            plural = ''
        return "%s hour%s ago" % (str(hours),plural)
    elif delta.seconds > 60:
        minutes = int(round(delta.seconds / 60.0))
        if minutes == 1:
            plural = ''
        return "%s minute%s ago" % (str(minutes),plural)
    else:
        return "just a moment ago"