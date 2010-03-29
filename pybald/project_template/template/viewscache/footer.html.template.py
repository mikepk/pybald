from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1259611340.390569
_template_filename='/usr/share/enerd/project_template/app/views/footer.html.template'
_template_uri='/footer.html.template'
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
        __M_writer(u'</div><!-- end main_content -->\n<div id="footer">\n<ul><li>Powered by PyBald &copy;2009 <a href="http://tenzerolab.com">TenZeroLab</a></li></ul>\n</div>\n</body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


