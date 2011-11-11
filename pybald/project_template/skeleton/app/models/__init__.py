#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by mikepk on 2010-10-14.
Copyright (c) 2011 Michael Kowalchik. All rights reserved.
"""

import os
import glob
import re

import project

# proj_path = project.path
project_path, top_level = os.path.split(project.path)

import pybald.db.models

__all__ = []
def load_models():
    models_path = __path__[0]
    # fully qualify the models with the project name
    match = re.search(r'([\d\w_]+)/app/models',models_path)
    if match:
        top_level = match.group(1)

    models = {}

    for modulefile in glob.iglob( os.path.join(models_path,"*.py") ):
        modname = re.search('(\w+)\.py',modulefile).group(1)
        if re.search(r'^\_',modname) or modname == 'init_db':
            continue
        # loads the modules in a relative fashion to this namespace
        # imp_modname = globals()['__name__']+'.'+modname
        imp_modname = top_level+".app.models."+modname
        temp =  __import__(imp_modname, globals(), locals(), [modname], -1)
        # HACKY, not sure I like this
        # avoid the double dot lookup
        globals()[modname] = getattr(temp,modname)
        __all__.append(modname)

def create():
    pybald.db.models.Base.metadata.create_all()

def drop():
    pybald.db.models.Base.metadata.drop_all()


load_models()

