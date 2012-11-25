#!/usr/bin/env python
# encoding: utf-8
# __init__.py
#
# Created by mikepk on 2009-07-24.
# Copyright (c) 2009 Michael Kowalchik. All rights reserved.

import sys
import os
import re

from inspect import isclass

class PybaldImportError(ImportError):
    pass

PYTHON_MODULE_NAME_PATTERN = re.compile(r'^([a-z][0-9a-z_]*)\.py$', re.I)
PYTHON_MAGIC_VARIABLE_PATTERN = re.compile(r'^__.*__$')
# TODO, use walk to have this recursively walk up the models path
# finding all interesting classes.
def pybald_class_loader(path, classes, module_globals, module_locals,
                                                               recursive=True):
    '''
    Take a set of special class names, a path, and scan the path loading classes
    that match or inherit from the list. Then these are returned into the provided
    module scope.

    This is used by pybald to search for special "Controller" classes to load
    into the router object for the entire project. It's also used to auto-load
    all models in the project under the models namespace for less typing.

    This is a somewhat expensive function so is only executed on first startup
    of the project.

    Note: The second auto-model loading use of this function  may be too
    "magical" and may be deprecated in a future release.

    :param path: The path to scan for matching classes.

    :param classes: A list of classes to use for matching.

    :param module_globals: The globals member of the package from which this
         method is called.

    :param module_locals: The locals member of the package from which this
         method is called.

    :param recursve: Whether to scan the path recursively looking for
         matching classes.
    '''
    loaded_classes = []
    for dirpath, dirnames, filenames in os.walk(path):
        print dirpath, path
        if dirpath != path:
            # turn nested path into package notation
            nested = os.path.relpath(dirpath, path
                                        ).replace('/', '.').lstrip('.')
        else:
            nested = None
        for filename in sorted(filenames):
            match = PYTHON_MODULE_NAME_PATTERN.search(filename)
            if not match:
                continue
            import_module_name = match.group(1)
            try:
                if not nested:
                    import_package_name = import_module_name
                    import_list = ()
                else:
                    import_list = (import_module_name,)
                    import_package_name = '.'.join((nested, import_module_name))
                scan_module = __import__(import_package_name,
                                         module_globals,
                                         module_locals,
                                         import_list,
                                         1)
            except ImportError, ie:
                ie.args = ("\nThe automatic pybald class loader "
                "failed while attempting to load the module {0} from {1}. "
                "Orignal message: {2}\n".format(filename, dirpath, ie.args[0]),)
                raise ie
            for classname in filter(lambda attribute_name: (
                    not PYTHON_MAGIC_VARIABLE_PATTERN.search(attribute_name) and
                                   attribute_name not in loaded_classes
                                   ),
                                                             dir(scan_module)):
                try:
                    module_class = getattr(scan_module, classname)
                    # only process class definitions from the modules
                    # not strictly necessary? Allow TypeError to catch non
                    # classes?
                    if not isclass(module_class):
                        continue
                    is_pybald_auto_loaded_module = issubclass(module_class,
                                                                       classes)
                # if the module member is not a class then skip
                except TypeError:
                    continue
                # if the module is one of the tracked class types
                # add the name to the provided scope
                if is_pybald_auto_loaded_module:
                    module_globals[classname] = module_class
                    loaded_classes.append(classname)
        if not recursive:
            break
    return loaded_classes
