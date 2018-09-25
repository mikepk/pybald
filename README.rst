Pybald
======

.. image:: https://travis-ci.org/mikepk/pybald.svg?branch=master
  :width: 90px
  :height: 20px
  :alt: Current Build Test State
  :target: https://travis-ci.org/mikepk/pybald

Pybald is a light weight, python, `MVC <https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_ style web framework. It is inspired by work done by `Ian Bicking <https://blog.ianbicking.org/>`_, and builds upon the concepts presented in `Another do-it-yourself framework <https://docs.pylonsproject.org/projects/webob/en/stable/do-it-yourself.html>`_. It is also takes design inspiration from `Ruby on Rails <http://rubyonrails.org>`_ and `Django <http://www.djangoproject.com/>`_. 

Pybald began life as an ultra-bare-bones framework but has evolved over time  adding convenience methods, components and glue:

  * `Routes <http://routes.groovie.org/>`_ for dispatching and URL parsing
  * `Mako <http://www.makotemplates.org/>`_ as the template engine.
  * `SqlAlchemy <http://sqlalchemy.org/>`_ for data persistence and object mapping
  * `WTForms <http://wtforms.readthedocs.io/en/latest/>`_ for automated form generation and validation
  * A more complex WSGI decorator
  * Some deploy infrastructure such as Apache and Nginx configuration templates
  * Session Management, Simple Logging, and template helper functions
