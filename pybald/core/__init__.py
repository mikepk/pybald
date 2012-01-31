#!/usr/bin/env python
# encoding: utf-8
# __init__.py
#
# Created by mikepk on 2009-07-24.
# Copyright (c) 2009 Michael Kowalchik. All rights reserved.

import os
import re

modname_pattern = re.compile(r'^([a-z]+[a-z_]*)\.py$', re.I)
# TODO, use walk to have this recursively walk up the models path
# finding all interesting classes.
def pybald_class_loader(path, classes, module_globals, module_locals, recursive=False):
    loaded_classes = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in sorted(filenames):
            match = modname_pattern.search(filename)
            if match:
                imp_modname = match.group(1)
                model_module = __import__(imp_modname, module_globals, module_locals, [], 1)
                for classname in dir(model_module):
                    if classname in loaded_classes:
                        continue
                    try:
                        module_class = getattr(model_module, classname)
                        pybald_model = issubclass(module_class, classes)
                    except TypeError:
                        # if the module member is not a class
                        continue
                    if pybald_model:
                        module_globals[classname] = module_class
                        loaded_classes.append(classname)
    return loaded_classes
