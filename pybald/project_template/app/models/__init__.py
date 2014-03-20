#!/usr/bin/env python
# encoding: utf-8
from pybald.db import models
from pybald.core import pybald_class_loader

models_path = __path__[0]
__all__ = pybald_class_loader(models_path, (models.Model, models.NonDbModel), globals(), locals())


def create():
    """Create all models, issuing SQL to create the required storage representation."""
    models.Base.metadata.create_all()
