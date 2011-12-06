#!/usr/bin/env python
# encoding: utf-8
import os
import glob
import re
from pybald.util import underscore_to_camel

__all__ = []
def load_controllers():
    for modulefile in glob.iglob( os.path.join(__path__[0],
                                               "*_controller.py") ):
        modname = re.search('(\w+_controller)\.py',modulefile).group(1)
        imp_modname = 'app.controllers.'+modname
        class_name = underscore_to_camel(modname)
        # print modname, class_name
        temp = __import__(modname, globals(), locals(), [modname], 1)
        __all__.append(modname)
load_controllers()