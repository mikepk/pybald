#!/usr/bin/env python
# encoding: utf-8

from wtforms import Form as WTForm
from wtforms import (StringField, TextAreaField, SelectField,
                     BooleanField, DateField, DateTimeField, FloatField,
                     IntegerField, FileField, RadioField, SelectMultipleField,
                     SubmitField, HiddenField, PasswordField, Field,
                     DecimalField)

from pybald.context import render
from pybald.core.helpers import HTMLLiteral


class MockParams(dict):
    def getlist(self, key):
        return [self[key]]

    def __repr__(self):
        return type(self).__name__ + '(' + dict.__repr__(self) + ')'


class Form(WTForm):
    class Meta:
        def render_field(self, field, render_kw):
            return HTMLLiteral(field.widget(field, **render_kw))

    def render(self, *pargs, **kargs):
        return HTMLLiteral(render.form_render('fieldset', format='form',
                                              fieldset=self))

FieldSet = Form
