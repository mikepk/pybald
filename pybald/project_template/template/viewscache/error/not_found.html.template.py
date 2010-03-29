from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1259611340.73157
_template_filename='/usr/share/enerd/project_template/app/views/error/not_found.html.template'
_template_uri='/error/not_found.html.template'
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
        __M_writer = context.writer()
        # SOURCE LINE 1
        runtime._include_file(context, '/header.html.template', _template_uri)
        __M_writer(u"\n<h1>Sorry, we can't find what you're looking for.</h1>\n<h2>You can always return to the ")
        # SOURCE LINE 3
        __M_writer(unicode(link_to("home page", 'home')))
        __M_writer(u' and try something else.</h2>\n')
        # SOURCE LINE 4
        runtime._include_file(context, '/footer.html.template', _template_uri)
        return ''
    finally:
        context.caller_stack._pop_frame()


