Routing and URLs
=================

The Pybald router is used to match web requests and URL's with application behaviors, specficially controllers and actions. It can also be used to *generate* urls symbolically inside of the application and templates to avoid hard coding paths inside of your application.

Pybald routes are defined explicitly using a forked version of the Routes python library.

Routing is defined using functions that accept a 'mapping object'. This mapping object is used to connect routes and define *submappers* (described later). The mapping object has a few methods, the most important of which is `connect`. Traditionally the convention is for the mapping object to be named `urls` and the function to be named `map`.

For simple projects, this function is usually defined in the `./app/urls.py` module.

Example
-------

Lets assume you want to create a route for `/blog/posts/45` to show a single blog post with an id, in this case 45. An example url route might look like the following:

.. code-block:: python

    def map(urls):
        urls.connect('show_post', r'/blog/posts/{id}', controller='blog', action='show')

The arguments to connect are the symbolic name for the route (show_post), the route itself (r'/blog/posts/{id}'), and then any variables that will be set when this route is matched. The r'' string format is a convention to use 'raw' strings without interpreting escape sequences. In this case we're setting the special controller and action variables so that the router will know which code to execute when this route is matched.

Capturing Variables
-------------------

This particular route has a 'capture variable', the {id} portion of the route. By using these variables, you can extract information from the URL to use in your request. This example will additionally set a variable named `id` in the request and set it to any value present in the url. For example, with a request like `/blog/posts/45` the variable id will be set to 45 when the request is processed.

Variable Requirements
---------------------

In the above example you may have noticed that this route match would potentially match on any value present on the url after `/blog/posts/`. If the request was `/blog/posts/frank`, the route would match and id would be `frank`. If, in your application, all ids are interger numbers, this might not be a case you want to have trigger your application behavior.

For this case you can use requirements in your variable captures. Requirements are regular expressions that can be used to limit what will be matched in the variable portion of your url route. Any standard regular expression can be used and would be added after a colon in the capture definition as follows:

.. code-block:: python

    def map(urls):
        urls.connect('show_post', r'/blog/posts/{id:\d+}', controller='blog', action='show')

Here we've added the requirement that there be one or more interger values after the url slash (and only interger values) to trigger the route match. This would match `/blog/posts/45` but not `/blog/posts/frank` or even `/blog/posts/45frank`.


RESTful Resources
-----------------

When creating CRUD applications, Pybald can automatically create a set of RESTful urls using the `collection` method on the mapper object.

.. code-block:: python

    def map(urls):
        urls.collection('posts', 'post', path_prefix=r'/blog',
        controller='blog')


=========== ======  ==============================
symbolic    method  url route
=========== ======  ==============================
posts       GET     /blog/posts{.format}          
create_post POST    /blog/posts{.format}          
new_post    GET     /blog/posts/new{.format}      
post        GET     /blog/posts/{id}{.format}     
update_post PUT     /blog/posts/{id}{.format}     
delete_post DELETE  /blog/posts/{id}{.format}     
edit_post   GET     /blog/posts/{id}/edit{.format}
=========== ======  ==============================

