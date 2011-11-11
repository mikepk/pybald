Pybald Core
===========


:mod:`templates` - template/view handling
-----------------------------------------

.. automodule:: pybald.core.templates

.. autoclass:: TemplateEngine
  :members: form_render, _get_template, __call__
  :undoc-members:


.. automodule:: pybald.core.controllers

:meth:`action` - decorator to turn methods into actions
-------------------------------------------------------

.. autofunction:: action

:class:`BaseController` - simple base class that pybald controllers can optionally subclass
-------------------------------------------------------------------------------------------

.. autoclass:: BaseController
  :members: index, _pre, _post, _redirect_to, _status, _not_found, _view
  :undoc-members:
  

:mod:`router` - pybald core, url dispatch, method munging, WSGI app
-------------------------------------------------------------------

.. automodule:: pybald.core.router
  
.. autoclass:: Router
  :members:

  .. automethod:: __call__
