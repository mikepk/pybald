Routing and URLs
=================

The Pybald router is used to match web requests and URL's with application behaviors, specficially controllers and actions. It can also be used to *generate* urls symbolically inside of the application and templates to avoid hard coding paths inside of your application.

Pybald routes are defined explicitly using a forked (and slightly modified) version of the `Routes <http://routes.readthedocs.org/en/latest/>`_ python library.

Defining Routes
---------------

Routing is defined using a function that accept a 'mapping object'. The Pybald router will accept this function and pass a mapping object in to construct the route table. This mapping object is used to connect routes and define *submappers* (described later). The mapping object has a few methods, the most important of which is `connect`. Traditionally the convention is for the mapping object to be named `urls` and the function to be named `map` but this is not strictly necessary.

For simple projects, this function is usually defined in the `PROJECT_NAME/app/urls.py` module.

Each route, when matched, will set a series of variables that will be used in routing the request and configuring the particular request. Of these variables, the two most important are `controller` and `action`. These two variables, when set, will tell the Pybald router what code will be executed when the match occurs. Other variables can be set, and those variables will be passed into the request to be processed.

Example
~~~~~~~

Lets assume you want to create a route for `/blog/posts/45` to show a single blog post with an id, in this case 45. An example route might look like the following:

.. code-block:: python

    def map(urls):
        urls.connect('show_post', r'/blog/posts/{id}', controller='posts',
                     action='show')

The arguments that are passed into connect are the symbolic name for the route (`show_post`), the route itself (`r'/blog/posts/{id}'`), and then any additional variables that will be set when this route is matched. The r'' string format prefix tells python to interpret the string as a `'raw' python string, where it will not interpret escape sequences (backslashes are left alone so \n will not create a newline) <https://docs.python.org/2/reference/lexical_analysis.html#string-literals>`_. In this case the controller and action variables are set to `posts` and `show`, respectively, which will tell Pybald which code will be executed on a match.

Capturing Variables
-------------------

This particular route also has a 'capture variable', the {id} portion of the above route. By using these capture variables, you can extract information from the URL to use in your request. This example will additionally set a variable named `id` in the request and set it to any value present in the url. For example, with a request like `/blog/posts/45` the variable id will be set to 45 when the request is processed.

Variable Requirements
~~~~~~~~~~~~~~~~~~~~~

In the above example you may have noticed that this route match could potentially match on any value present on the url after `/blog/posts/`. If the request was `/blog/posts/frank`, the route would match and id would be `frank`. If, in your application, all ids are interger numbers, this might not be a case you want to have trigger your application behavior.

For this case you can use requirements in your variable captures. Requirements are regular expressions that can be used to limit what will be matched in the variable portion of your url route. Any standard regular expression can be used and would be added after a colon in the capture definition as follows:

.. code-block:: python

    def map(urls):
        urls.connect('show_post', r'/blog/posts/{id:\d+}', controller='posts',
                     action='show')

Here we've added the requirement that there be one or more interger values after the url slash (and only interger values) to trigger the route match. This would match `/blog/posts/45` but not `/blog/posts/frank` or even `/blog/posts/45frank`.


RESTful Resources
-----------------

When creating CRUD applications, Pybald (via the Routes library) can automatically create a set of RESTful urls using the `collection` method on the mapper object.

.. code-block:: python

    def map(urls):
        urls.collection('posts', 'post', path_prefix=r'/blog',
                        controller='posts')


The collection method will create the following routes mapping to a series of default HTTP methods and actions.

=========== ======  ======  ==============================
symbolic    method  action  url route
=========== ======  ======  ==============================
posts       GET     index   /blog/posts{.format}          
create_post POST    create  /blog/posts{.format}          
new_post    GET     new     /blog/posts/new{.format}      
post        GET     show    /blog/posts/{id}{.format}     
update_post PUT     update  /blog/posts/{id}{.format}     
delete_post DELETE  delete  /blog/posts/{id}{.format}     
edit_post   GET     edit    /blog/posts/{id}/edit{.format}
=========== ======  ======  ==============================

These follow some standard REST conventions (using PUT for updates, DELETE for deletes etc) while adding `new` and `edit` actions that are generally used to map to forms for creating new resources or editing existing resources.
