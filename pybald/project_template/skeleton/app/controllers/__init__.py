#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

This module is part of pybald. 
"""

import os
import glob
import re

__all__ = []
def load_controllers():
    for modulefile in glob.iglob( os.path.join(__path__[0],"*Controller.py") ):
        modname = re.search('(\w+Controller)\.py',modulefile).group(1)
        imp_modname = 'app.controllers.'+modname
        temp = __import__(imp_modname, globals(), locals(), [modname], -1)
        shortname = re.search('(\w+)Controller',modname).group(1)
        if shortname:
            globals()[shortname] = getattr(temp, modname)
        # print temp
        
        __all__.append(modname)
load_controllers()