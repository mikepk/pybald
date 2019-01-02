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
from six.moves.urllib.parse import urlparse, ParseResult
import re
from routes import request_config
from pybald import context
import logging
log = logging.getLogger(__name__)

try:
    import pyhash
    hashfunc = pyhash.super_fast_hash()
except ImportError:
    log.warning("-"*80 + '''
    Warning
    -------
    Using python built-in hash() for asset URL generation. This is system
    implementation specific and may result in different hosts mapping static
    assets to different static hosts. That may cause inefficient use of browser
    caches. Optionally you can install pyhash to install additional fast,
    non-cryptographic, hashes that are not system dependent.

    pip install pyhash
'''+"-"*80)
    hashfunc = hash

try:
    type(unicode)
except NameError:
    unicode = str


# parse result keys
class AssetUrl(dict):
    '''
    Wraps urls and returns URL transformations when necessary.

    The primary use case is transforming the url for running static assets on a CDN.
    '''
    keys = ("scheme", "netloc", "path", "params", "query", "fragment")

    def __init__(self, url):
        self.raw_url = url
        super(AssetUrl, self).__init__(**dict(zip(self.keys, urlparse(url))))

    def __str__(self):
        return self.__html__()

    def __html__(self):
        '''Return a transformed URL if necessary (appending protocol and CDN)'''
        host = self.get('netloc', None)
        # Don't CDN urls with hosts we're not re-writing
        if host:
            if (context.config.STATIC_SOURCES is None or
                                           host not in context.config.STATIC_SOURCES):
                return self.raw_url
        if (context.config.USE_CDN and (context.config.CDN_HOST or context.config.STATIC_HOSTS)):
            # get the protocol for the current request
            # this requires the custom HTTP header X-Forwarded-Proto
            # set if running behind a proxy (or if SSL is terminated
            # upstream)
            try:
                protocol = request_config().protocol
            except AttributeError:
                # are we not in a request? Use a default protocol
                protocol = context.config.DEFAULT_PROTOCOL
            # use the round robin hosts to speed download when not https
            if protocol != "https" and context.config.STATIC_HOSTS:
                self['netloc'] = context.config.STATIC_HOSTS[hashfunc(self.raw_url) %
                                                      len(context.config.STATIC_HOSTS)]
            else:
                self['netloc'] = context.config.CDN_HOST
            # adjust the scheme of any link with a net location
            # to match the current request so we don't have mixed link
            # protocols
            if self['netloc']:
                self['scheme'] = protocol
        return ParseResult(**self).geturl()


class HTMLLiteral(unicode):
    '''This is an object to handle literal HTML in Mako template'''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.__html__()

    def __html__(self):
        return self.value


class as_p(object):
    def __init__(self, input_str):
        self.str_value = input_str

    def __str__(self):
        return self.__html__()

    def __html__(self):
        '''Return the image in string form.'''
        lines = self.str_value.splitlines()
        return u"".join([u"<p>{0}</p>".format(line) for line in lines])


class tag(object):
    def set(self, **kargs):
        self.attribs.extend([u'''{0}="{1}"'''.format(k.rstrip('_'), v) for k, v in kargs.items()])
        return self


class img(tag):
    def __init__(self, src='', **kargs):
        self.img_src = src
        self.attribs = []
        self.set(**kargs)
        if "alt" not in kargs:
            self.set(alt=self.img_src)

    def __str__(self):
        return self.__html__()

    def __html__(self):
        '''Return the image in string form.'''
        return u'''<img src="{0}" {1} />'''.format(AssetUrl(str(self.img_src)),
                                                   " ".join(self.attribs))


class anchor(tag):
    def __init__(self, link_text='', name='', **kargs):
        self.link_text = filters.html_escape(link_text)
        if name:
            self.url = name
        else:
            self.url = self.link_text
        self.attribs = []
        self.set(**kargs)

    def __str__(self):
        return self.__html__()

    def __html__(self):
        '''Return the anchor in string form.'''
        # attr = " ".join(self.attribs)
        return u'''<a name="{0}" {1}>{2}</a>'''.format(self.url,
                                                       " ".join(self.attribs),
                                                       self.link_text)


class link(tag):
    def __init__(self, link_text='', **kargs):
        self.link_text = filters.html_escape(link_text)
        self.url = "#"
        self.attribs = []
        self.set(**kargs)

    def filter(self, filter_type="h"):
        self.link_text = filters.html_escape(self.link_text)
        return self

    def to(self, *pargs, **kargs):
        self.url = url_for(*pargs, **kargs)
        return self

    def to_raw_url(self, url):
        # Link directly with no url_for processing
        # (url_for can't deal with unicode!)
        self.url = url
        return self

    def __str__(self):
        return self.__html__()

    def __html__(self):
        '''Return the link in string form.'''
        attr = " ".join(self.attribs)
        return u'''<a href="{0}" {1}>{2}</a>'''.format(self.url, attr, self.link_text)


def plural(list_object):
    '''Return "s" for > 1 items'''
    if len(list_object) > 1:
        return "s"
    else:
        return ""


FRACTIONAL_SECOND = re.compile(r'\.\d+$')


def humanize(date_string, relative_date=None):
    '''Convert a date string into a 'humanized' relative string (like 1 day ago)'''
    date_format = "%Y-%m-%d %H:%M:%S"
    # strip decimal second precision
    date_string = FRACTIONAL_SECOND.sub('', date_string)
    try:
        date = datetime.strptime(date_string, date_format)
    except Exception:
        # if the date string format doesn't match, just return it
        return date_string
    if relative_date is None:
        now = datetime.now()
    else:
        now = relative_date
    delta = now - date
    plural = 's'
    if delta.days < 0:
        return "in the future"
    elif delta.days >= 30:
        date_format = "%d %b"
        if date.year != now.year:
            date_format += " '%y"
        return str(date.strftime(date_format).lstrip('0'))
    elif delta.days >= 14:
        weeks = delta.days / 7
        if weeks == 1:
            plural = ''
        return "%s week%s ago" % (str(int(weeks)), plural)
    elif delta.days >= 1:
        if delta.days == 1:
            plural = ''
        return "%s day%s ago" % (str(delta.days), plural)
    # > 1 hour, display in hours
    elif delta.seconds > 3600:
        hours = int(round(delta.seconds / 3600.0))
        if hours == 1:
            plural = ''
        return "%s hour%s ago" % (str(hours), plural)
    elif delta.seconds > 60:
        minutes = int(round(delta.seconds / 60.0))
        if minutes == 1:
            plural = ''
        return "%s minute%s ago" % (str(minutes), plural)
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
              tuple([(chr(ascii_val), r"\u{:04X}".format(ascii_val)) for ascii_val in range(32)]))


def js_escape(value):
    """
    Hex encodes characters for use in JavaScript strings.
    (from django.utils.html)
    """
    if value:
        for bad, good in _js_escapes:
            value = value.replace(bad, good)
    return value
