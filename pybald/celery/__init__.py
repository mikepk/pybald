"""
Automatically sets the environment variable `CELERY_LOADER` to
`pybald.celerey.loader:PybaldLoader`.  This ensures the loader is
specified when accessing the rest of this package, and allows celery
to be installed in a webapp just by importing pybald.celery::

    import pybald.celery

"""
import os
import warnings

CELERYPYBALD_LOADER = 'pybald.celery.loader.PybaldLoader'
if os.environ.get('CELERY_LOADER', CELERYPYBALD_LOADER) != CELERYPYBALD_LOADER:
    warnings.warn("'CELERY_LOADER' environment variable will be overridden by pybald.celery.")
os.environ['CELERY_LOADER'] = CELERYPYBALD_LOADER
