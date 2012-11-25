.. Pybald documentation master file, created by
   sphinx-quickstart on Tue Apr 13 12:00:54 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. warning::

    This documentation is under construction and is in no way complete (and may be grossly wrong). If you're interested in this project, please contact me before reading any further. mikepk tenzerolab.com.

Introduction
============

Pybald is a light weight, python, `MVC <http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_ style web framework. It is inspired by work done by `Ian Bicking <http://blog.ianbicking.org/>`_, and builds upon the concepts presented in `Another do-it-yourself framework <http://pythonpaste.org/webob/do-it-yourself.html>`_. It is also takes design inspiration from `Ruby on Rails <http://rubyonrails.org>`_ and `Django <http://www.djangoproject.com/>`_. It's something of a spiritual successor to Pylons.

Pybald began life as an ultra-bare-bones framework but has evolved over time  adding convenience methods, components and glue:

  * `Routes <http://routes.groovie.org/>`_ for dispatching and URL parsing
  * `Mako <http://www.makotemplates.org/>`_ as the template engine.
  * `SqlAlchemy <http://sqlalchemy.org/>`_ for data persistence and object mapping
  * `FormAlchemy <http://formalchemy.org/>`_ for automated form generation and validation
  * A more complex WSGI decorator
  * Some deploy infrastructure such as Apache and Nginx configuration templates
  * Session Management, Simple Logging, and template helper functions


.. toctree::
  :maxdepth: 2
  :hidden:

  intro
  getting_started
  using
  running_an_app
  magic
  configuration
  routing
  controllers
  models
  forms
  error_handling
  api_reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

License
=======

Pybald is distributed under the `MIT license <http://www.opensource.org/licenses/mit-license.php>`_.

.. literalinclude:: ../LICENSE
