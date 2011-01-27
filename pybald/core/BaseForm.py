#!/usr/bin/env python
# encoding: utf-8
"""
BaseForm.py

Created by mikepk on 2010-04-25.
Copyright (c) 2010 Michael Kowalchik. All rights reserved.
"""

import os
from formalchemy import FieldSet

import project
from formalchemy import templates, config
from pybald.core.TemplateEngine import engine

import pybald.db.models
# templates.MAKO_TEMPLATES

# set the Pybald Mako engine to be the main
# form template engine
config.engine = engine.form_render

class BaseForm(FieldSet):
    def __init__(self, *pargs, **kargs):

        template = kargs.get('template', None)
        if template:
            del kargs['template']
        else:
            template = 'fieldset'
            
        # This hack is to assign a session for non-instances. Used primarily for
        # loading the relations in models, otherwise session has to be explicitly
        # assigned (I think, can't find docs to the contrary)
        if isinstance(pargs[0],pybald.db.models.ModelMeta) and not kargs.get('session',None):
            kargs['session'] = pybald.db.models.session

        super(BaseForm,self).__init__(*pargs,**kargs)
        # FieldSet.__init__(self,instance or self.__class__, data=data or None)
        # set the template_id to the name of the model
        self.template_id = os.path.join('forms', template)
        
