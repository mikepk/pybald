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
    pybald.configure(default=True)

    def map(urls):
        urls.connect('home', r'/', controller='home')

    class HomeController(Controller):
        @action
        def index(self, req):
            return "Hello!"

    app = Router(routes=map, controllers=[HomeController])

    if __name__ == "__main__":
        context.start(app)

This mini application illustrates many of the core concepts present in most Pybald applications. These include: configuring an application and the pybald `context`, setting up URL routes via a mapping function, creating a controller class with a a handler using the :ref:`action decorator <actions>` and finally setting up a WSGI pipeline using the pybald Router. Each of these topics will be covered in more detail in the following documentation.

Other core concepts like templating, data persistence and models will be also be covered later.


Contents
==========

.. toctree::
  :maxdepth: 2

  intro
  getting_started
  configuration
  routing
  using
  magic
  templates
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

Dependencies
============

Pybald works with Python 2.7 and Python 3 verions above and including 3.5.

Pybald currently depends on, and will automatically install, the following libraries:

* `Mako Templates <http://www.makotemplates.org/>`_
* `Routes <https://routes.readthedocs.io/en/latest/>`_
* `WebOb <https://webob.org/>`_
* `SqlAlchemy <http://sqlalchemy.org/>`_
* `WTForms <https://wtforms.readthedocs.org/en/latest/>`_

These libraries are well tested and generally very well documented. When expanding beyond the simplest use cases presented in this documentation, you can dive deeper and access more functionality by exploring each library's individual docs.

License
=======

Pybald is distributed under the `MIT license <http://www.opensource.org/licenses/mit-license.php>`_.

.. literalinclude:: ../LICENSE
   :language: none