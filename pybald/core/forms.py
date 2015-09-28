#!/usr/bin/env python
# encoding: utf-8

from wtforms import Form as WTForm
from wtforms import (StringField, TextAreaField, DecimalField, SelectField,
                     BooleanField, DateField, DateTimeField, FloatField,
                     IntegerField, FileField, RadioField, SelectMultipleField,
                     SubmitField, HiddenField, PasswordField, Field)
from wtforms import validators

# from pybald import context
from pybald.context import render
from pybald.core.helpers import HTMLLiteral

# from pybald.db import models



class Form(WTForm):
    class Meta:
        def render_field(cls, field, render_kw):
            return HTMLLiteral(field.widget(field, **render_kw))

    def render(self, *pargs, **kargs):
        return HTMLLiteral(render.form_render('fieldset', format='form', fieldset=self))

FieldSet = Form