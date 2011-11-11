Introduction
============

PyBald is a extremely light weight, python, `MVC <http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_ web framework that is inspired by work done by `Ian Bicking <http://blog.ianbicking.org/>`_, and builds upon the concepts presented in `Another do-it-yourself framework <http://pythonpaste.org/webob/do-it-yourself.html>`_. It is also takes some design inspiration from `Ruby on Rails <http://rubyonrails.org>`_ and `Django <http://www.djangoproject.com/>`_. 

It takes a bare-bones framework approach and adds some convenience methods and the following components and glue:

  * `Routes <http://routes.groovie.org/>`_ for dispatching and URL parsing
  * `Mako <http://www.makotemplates.org/>`_ as the template engine.
  * `SqlAlchemy <http://sqlalchemy.org/>`_ for data persistence and object mapping
  * `FormAlchemy <http://formalchemy.org/>`_ for automated form generation and validation
  * A slightly more complex WSGI decorator
  * Apache and Nginx configuration templates
  * Session Management, Simple Logging, and some template helper functions

Goals
-----

PyBald was built initially as an exploration of what makes up a modern web framework. It was not intended to be "industrial strength" but more as a way to learn the various components of a web framework, how they fit together, and a way to play with those pieces. After spending time with PyBald, I've found the basic framework to be very clean and light on initial configuration and relatively powerful since it heavily leverages the `WSGI <http://wsgi.org/wsgi/>`_ interface. The way the system is setup, you can use the various 'helper' functions of the framework, but are not limited to using them if you don't want to. The framework tries to be somewhat 'pythonic' by having you explicitly invoke the pieces that you want to use (via the WSGI pipeline and action decorators). This allows you to pick and choose the pieces you want to use, or even drop down to the basic WSGI interface.

This framework also stems from a slight annoyance that many existing frameworks require large configuration files to generate python code. It's my contention that one of the primary benefits of Python code is its readability, so in some sense the configuration should ***be*** the code. This is especially true for activities like setting up the WSGI pipeline.

The goals behind PyBald:

* Fast and easy startup - get running quickly with limited configuration
* Brevity and clarity - build the basics of a python web framework core without a lot of complex code. Make it easy to learn and hack.
* Limited, or at least transparent, "Magic" - A lot of frameworks provide behaviors that seem "magical" without making clear how that magic is accomplished. PyBald tries to keep most of it's magic brief, easily accessible, and usually explicitly invoked.
* Stick to `convention over configuration <http://en.wikipedia.org/wiki/Convention_over_configuration>`_
* Use `WSGI <http://wsgi.org/wsgi/>`_ for the web interfaces and utilize WSGI middleware

What PyBald is **not**\ :

* Not Battle Tested
* Not Performance Tested
* Not Designed to be ***uber*** configurable (that's covered nicely by `Pylons <http://pylonshq.com>`_) - you could hack in another template engine or url dispatcher fairly easily but it was not a goal of the project

Requirements
------------

It has only been tested on Python 2.5 and 2.6.

PyBald currently requires the following packages:

* `Mako Templates <http://www.makotemplates.org/>`_
* `Routes <http://routes.groovie.org/>`_
* `WebOb <http://pythonpaste.org/webob/>`_
* `Paste <http://pythonpaste.org/>`_
* `SqlAlchemy <http://sqlalchemy.org/>`_
* `FormAlchemy <http://formalchemy.org/>`_

