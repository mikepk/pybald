#!/usr/bin/env python
# encoding: utf-8

import os

import project
from formalchemy import templates, config
from formalchemy import FieldSet, Field, Grid, validators

from pybald.core.templates import engine

import pybald.db.models
import inspect

# set the Pybald Mako engine to be the main
# form template engine
config.engine = engine.form_render


class BaseForm(FieldSet):
    def __init__(self, *pargs, **kargs):

        template = kargs.pop('template', 'fieldset')

        # This hack is to assign a session for non-instances. Used
        # primarily for loading the relations in models, otherwise
        # session has to be explicitly assigned (I think, can't find
        # docs to the contrary)
        if (pargs and isinstance(pargs[0], pybald.db.models.ModelMeta) and not
            'session' in kargs):
            kargs['session'] = pybald.db.models.session

        # Init the standard FieldSet
        super(BaseForm, self).__init__(*pargs, **kargs)
        # FieldSet.__init__(self,instance or self.__class__, data=data or None)
        # set the template_id to the name of the model
        self.template_id = os.path.join('forms', template)


class MultiFieldSet(object):
    def __init__(self, *pargs, **kargs):
        self.fieldsets = []
        if pargs and inspect.isclass(pargs[0]):
            klass_name = pargs[0].__name__
        else:
            raise ValueError("SA Class required, instances not supported")

        self.fieldset_key = ''.join([klass_name, '--'])
        data = kargs.pop('data', None)
        if data is not None:
            keys = filter(lambda x: x.startswith(self.fieldset_key),
                                                                set(data.keys()))

            try:
                fields = [zip([key] * len(data.getall(key)), data.getall(key))
                                             for key in keys]
            except AttributeError:
                raise TypeError("data argument must support 'getall(key)' like WebOb MultiDict")

            transposed = zip(*fields)

            for data in [dict(x) for x in transposed]:
                self.fieldsets.append(BaseForm(data=data, *pargs, **kargs))
        else:
            self.fieldsets.append(BaseForm(data=None, *pargs, **kargs))

    def __iter__(self):
        '''Iterator to return fieldset groups'''
        for fieldset in self.fieldsets:
            yield fieldset

