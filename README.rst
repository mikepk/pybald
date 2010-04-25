PyBald
======

PyBald is a extremely light weight, python, `MVC <http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_ web framework that is inspired by work done by `Ian Bicking <http://blog.ianbicking.org/>`_, and builds upon the concepts presented in `Another do-it-yourself framework <http://pythonpaste.org/webob/do-it-yourself.html>`_. It takes the bare-bones framework approach presented there and adds some convenience methods and the following components and glue:

  * `Routes <http://routes.groovie.org/>`_ for dispatching and URL parsing
  * `Mako <http://www.makotemplates.org/>`_ as the template engine.
  * A very thin MySQL interface and python object to database table mapper
  * `SqlAlchemy <http://www.sqlalchemy.org/>`_ integration
  * Automated forms using `FormAlchemy <http://code.google.com/p/formalchemy/>`_
  * A slightly more complex WSGI decorator
  * An Apache configuration template
  * Session Management, Simple Logging, and some template helper functions
  
License
=======

PyBald is distributed under the `MIT license <http://www.opensource.org/licenses/mit-license.php>`_. See LICENSE.
