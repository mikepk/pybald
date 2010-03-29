from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1259611340.384995
_template_filename='/usr/share/enerd/project_template/app/views/header.html.template'
_template_uri='/header.html.template'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from routes import url_for
from pybald.core.helpers import link_to
from pybald.core.helpers import link_img_to
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        page = context.get('page', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n\t"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n<title>')
        # SOURCE LINE 7
        if page['title']: 
            # SOURCE LINE 8
            __M_writer(unicode(page['title']))
            __M_writer(u' &mdash; PyBald')
            # SOURCE LINE 9
        else: 
            # SOURCE LINE 10
            __M_writer(u'PyBald')
        # SOURCE LINE 12
        __M_writer(u'</title>\n<link rel="stylesheet" type="text/css" media="screen" href="/css/site.css" />\n<script type="text/javascript" src="/js/jquery-1.3.2.min.js"></script>\n')
        # SOURCE LINE 15
        if page['headers']:
            # SOURCE LINE 16
            for head in page['headers']:
                # SOURCE LINE 17
                __M_writer(unicode(head))
                __M_writer(u'\n')
        # SOURCE LINE 20
        __M_writer(u'</head>\n<body>\n<div id="main_content">\n<div id="banner">\n')
        # SOURCE LINE 24
        __M_writer(unicode(link_img_to('/images/pybald.png','home', alt="PyBald", style_id="logo")))
        __M_writer(u'\n<div class="clear"><!-- --></div>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


