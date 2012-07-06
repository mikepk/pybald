#!/usr/bin/env python
# encoding: utf-8

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

# from markdown import markdown

def as_p(input_str):
    lines = input_str.splitlines()
    return unicode("".join([u"<p>{0}</p>".format(line) for line in lines]))

class tag(object):
    def set(self, **kargs):
        self.attribs.extend([u'''{0}="{1}"'''.format(k.rstrip('_'), v) for k,v in kargs.items() ])
        return self


class img(tag):
    def __init__(self,src='', **kargs):
        self.img_src = src
        self.attribs = []
        self.set(**kargs)
        if "alt" not in kargs:
            self.set(alt=self.img_src)

    def __str__(self):
        '''Return the image in string form.'''
        return u'''<img src="{0}" {1} />'''.format(self.img_src, " ".join(self.attribs) )


class anchor(tag):
    def __init__(self,link_text='', name='', **kargs):
        self.link_text = link_text
        if name:
            self.url = name
        else:
            self.url=self.link_text
        self.attribs = []
        self.set(**kargs)

    def __str__(self):
        '''Return the anchor in string form.'''
        attr = " ".join(self.attribs)
        return u'''<a name="{0}" {1}>{2}</a>'''.format(self.url,
                                                       " ".join(self.attribs),
                                                       self.link_text)


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
        attr = " ".join(self.attribs)
        return u'''<a href="{0}" {1}>{2}</a>'''.format(self.url, attr, self.link_text)

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
    if delta.days < 0:
        return "in the future"
    elif delta.days >= 1:
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

# From django.utils.html: Javascript escape characters
_base_js_escapes = (
    ('\\', '\\u005C'),
    ('\'', '\\u0027'),
    ('"', '\\u0022'),
    ('>', '\\u003E'),
    ('<', '\\u003C'),
    ('&', '\\u0026'),
    ('=', '\\u003D'),
    ('-', '\\u002D'),
    (';', '\\u003B'),
    ('\u2028', '\\u2028'),
    ('\u2029', '\\u2029')
)

# From django.utils.html: Escape every ASCII character with a value less than 32.
_js_escapes = (_base_js_escapes +
               tuple([('%c' % z, '\\u%04X' % z) for z in range(32)]))

def js_escape(value):
    """
    Hex encodes characters for use in JavaScript strings.
    (from django.utils.html)
    """
    if value:
        for bad, good in _js_escapes:
            value = value.replace(bad, good)
    return value
