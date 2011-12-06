#!/usr/bin/env python
# encoding: utf-8
import os
import glob
import re

import project

# proj_path = project.path
project_path, top_level = os.path.split(project.path)

import pybald.db.models
from pybald.util import underscore_to_camel

__all__ = []

modname_pattern = re.compile(r'(\w+)\.py')
def load_models():
    """Load the models and assign them to the module namespace.
    
    Scan the app/models path for models. Import them and then use a shorthand
    name to assign it to the module's global namespace.
    
    """
    models_path = __path__[0]
    # fully qualify the models with the project name
    match = re.search(r'([\d\w_]+)/app/models',models_path)
    if match:
        top_level = match.group(1)

    for modulefile in sorted(glob.iglob( os.path.join(models_path,"*.py") )):
        # print modulefile

        modname = modname_pattern.search(modulefile).group(1)
        if re.search(r'^\_',modname) or modname == 'init_db':
            continue

        class_name = underscore_to_camel(modname)
        # loads the modules in a relative fashion to this namespace
        # imp_modname = globals()['__name__']+'.'+modname
        # imp_modname = "quiz_site.app.models."+modname
        if class_name in __all__:
            continue
        imp_modname = modname
        # print imp_modname
        temp =  __import__(imp_modname, globals(), locals(), [modname], 1)
        # HACKY, not sure I like this
        # avoid the double dot lookup
        globals()[class_name] = getattr(temp, class_name)
        __all__.append(class_name)

def create():
    """Create all models, issuing SQL to create the required storage representation."""
    Base.metadata.create_all()

load_models()
