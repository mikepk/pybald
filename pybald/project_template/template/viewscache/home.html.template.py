from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1259611340.3577509
_template_filename='/usr/share/enerd/project_template/app/views/home.html.template'
_template_uri='/home.html.template'
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
        message = context.get('message', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        runtime._include_file(context, 'header.html.template', _template_uri)
        __M_writer(u'\n<div id="main_page">\n<h1>Congratulations, PyBald appears to be working properly.</h1>\n<h2>')
        # SOURCE LINE 4
        __M_writer(unicode(message))
        __M_writer(u'</h2>\n</div>\n')
        # SOURCE LINE 6
        runtime._include_file(context, 'footer.html.template', _template_uri)
        return ''
    finally:
        context.caller_stack._pop_frame()


