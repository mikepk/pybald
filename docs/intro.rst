Introduction
============

Overview and Goals
------------------

*For lazy hackers that know what they're doing.*

Pybald was built initially as an exploration of what makes up a modern web framework. It was not intended to be "industrial strength" but more as a way to experiment with various python web components and how they fit together. After being used to build some non-trivial web projects, Pybald has evolved from this early incarnation to be a fairly complete web framework with it's own personality. It's still very clean and light on initial configuration but it is also relatively powerful since it makes use of many "best-of-breed" components connected together using the `WSGI <http://wsgi.org/wsgi/>`_ interface. 

The goals behind Pybald:

* Fast and easy startup - get running quickly with limited configuration
* Brevity and clarity - build the basics of a python web framework core without a lot of complex code. Make it easy to learn and hack.
* Opinionated but hackable - one set of components is "official" and installed by default but the system is not a black box
* Support quick prototyping, but don't limit options as a project grows
* Stick to `convention over configuration <http://en.wikipedia.org/wiki/Convention_over_configuration>`_
* Limited, or at least transparent, "Magic" - A lot of frameworks provide behaviors that seem "magical" without making clear how that magic is accomplished. Pybald's "magic" is limited, easily accessible, and usually explicitly invoked.
* Use `WSGI <http://wsgi.org/wsgi/>`_ for the web interfaces and utilize WSGI middleware

What Pybald is **not**\ :

* Not Designed for maximum configurability. It's relatively trivial to use a different template engine or url dispatcher but that's not the goal of the project. There are other frameworks that serve that need like `Pylons / Pyramid <http://pylonshq.com>`_ 

Dependencies
------------

It has only been tested on Python 2.5 and 2.6.

Pybald currently depends on, and will automatically install, the following projects:

* `Mako Templates <http://www.makotemplates.org/>`_
* `Routes <http://routes.groovie.org/>`_
* `WebOb <http://pythonpaste.org/webob/>`_
* `Paste <http://pythonpaste.org/>`_
* `SqlAlchemy <http://sqlalchemy.org/>`_
* `FormAlchemy <http://formalchemy.org/>`_

