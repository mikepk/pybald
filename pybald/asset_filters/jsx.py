from __future__ import print_function
# import os
# import subprocess

from webassets.filter import Filter
from webassets.exceptions import FilterError

from react import jsx

class JsxFilter(Filter):
    name = 'jsx'
    max_debug_level = None

    def output(self, _in, out, **kwargs):
        out.write(jsx.transform_string(_in.read().encode('utf-8')))
