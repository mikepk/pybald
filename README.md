# Pybald

[![Current Build Test
State](https://travis-ci.org/mikepk/pybald.svg?branch=master)](https://travis-ci.org/mikepk/pybald)

Pybald is a light weight, python, [MVC](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) style
web framework. It is inspired by work done by [Ian
Bicking](https://blog.ianbicking.org/), and builds upon the concepts
presented in [Another do-it-yourself
framework](https://docs.pylonsproject.org/projects/webob/en/stable/do-it-yourself.html).
It is also takes design inspiration from [Ruby on
Rails](http://rubyonrails.org) and
[Django](http://www.djangoproject.com/).

[The in-progress documentation](http://pybald.com/)

Pybald began life as an ultra-bare-bones framework but has evolved over
time adding convenience methods, components and glue:

>   - [Routes](https://routes.readthedocs.io/en/latest/) for dispatching
>     and URL parsing
>   - [Mako](https://www.makotemplates.org/) as the template engine.
>   - [SqlAlchemy](https://sqlalchemy.org/) for data persistence and
>     object mapping
>   - [WTForms](https://wtforms.readthedocs.io/en/latest/) for automated
>     form generation and validation
>   - A more complex WSGI decorator
>   - Some deploy infrastructure such as Apache and Nginx configuration
>     templates
>   - Session Management, Simple Logging, and template helper functions

