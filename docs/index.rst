.. Pybald documentation master file, created by
   sphinx-quickstart on Tue Apr 13 12:00:54 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pybald
============

Pybald is an `MVC <http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_ style web framework written in `Python <http://python.org>`_. It is inspired by work done by `Ian Bicking <http://blog.ianbicking.org/>`_, and builds upon the concepts presented in `Another do-it-yourself framework <http://pythonpaste.org/webob/do-it-yourself.html>`_. It also takes some design inspiration from `Ruby on Rails <http://rubyonrails.org>`_, `Django <http://www.djangoproject.com/>`_, and `Flask <http://flask.pocoo.org/>`_.


A Small Pybald Application
==========================


.. code-block:: python

    import pybald
    from pybald import context
    from pybald.core.controllers import Controller, action
    from pybald.core.router import Router

    # configure our pybald application
    pybald.configure()

    def map(urls):
        urls.connect('home', r'/', controller='home')

    class HomeController(Controller):
        @action
        def index(self, req):
            return "Hello!"

    app = Router(routes=map, controllers=[HomeController])

    if __name__ == "__main__":
        context.start(app)

This mini application illustrates four of the five core concepts present in most Pybald applications. These include: configuring an application and the pybald `context`, setting up URL routes via a mapping function, creating a controller class with a a handler using the :ref:`action decorator <actions>` and finally setting up a WSGI pipeline using the pybald Router. Each of these topics will be covered in more detail in the following documentation.

The final core concept, data persistence and models will be covered later.


Contents
==========

.. toctree::
  :maxdepth: 2

  intro
  dependencies
  getting_started
  using
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
