Background
==========

Why?
----

If I had to summarize the basic philosophy of Pybald it would be the following it is *for lazy hackers that know what they're doing.*

Pybald was built initially as an exploration of what makes up a modern web framework. It was not originally intended to be "industrial strength" but as a way to experiment with various python web components and how they fit together. After being used to build some non-trivial web projects, Pybald has evolved from this early incarnation to be a fairly complete web framework with its own personality. It's still clean and light on initial configuration but it is also relatively powerful since it makes use of many "best-of-breed" components from the Python ecosystem and uses consistent interfaes like the `WSGI <http://wsgi.readthedocs.org/en/latest/>`_ interface. 

The goals behind Pybald:

* Fast and easy startup - get running quickly with limited configuration and sane defaults to minimize initial required decisions
* Brevity and clarity - build the basics of a python web framework core without a lot of complex code. Make it easy to learn and hack.
* Opinionated but hackable - one set of components is "official" and installed by default but the system is not a black box
* More *batteries* *included* than micro frameworks like Flask, but not not as monolithic as some other frameworks. "Batteries" are more often than not taken from the Python ecosystem and incorporated rather than custom solutions
* Support quick prototyping, but don't limit options as a project grows
* Strike a balance of explicit vs `convention over configuration <http://en.wikipedia.org/wiki/Convention_over_configuration>`_
* Limited, or at least transparent, "Magic" - A lot of frameworks provide behaviors that seem "magical" without making clear how that magic is accomplished. Pybald's "magic" is limited, easily accessible, and usually explicitly invoked
* Keep the interfaces simple and accessible, i.e. use `WSGI <http://wsgi.readthedocs.org/en/latest/>`_ for the web interfaces and utilize WSGI middleware
* *Don't coddle me* - give the developer the power to execute logic in the templates, don't hide RDBMS implementation details and SQL, give (easy) access to the internals of the framework, give developers power and flexibility and don't impose design hygine

What Pybald is **not**\ :

* Not Designed for maximum configurability. It's relatively trivial to use a different template engine or url dispatcher but that's not the goal of the project. There are other frameworks that serve that need like `Pylons / Pyramid <http://www.pylonsproject.org/>`_ 


