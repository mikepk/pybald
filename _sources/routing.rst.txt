Routing and URLs
=================

The Pybald router is the 'core' of Pybald and is a WSGI application. It is used to match web requests and URL's with application behaviors. The router is configured by using a *URL mapping* and a list of potential controllers. The URL mapping can also be used to *generate* urls symbolically inside of the application and templates to avoid hard coding paths inside of your application.

Pybald url routes are defined explicitly. The Pybald router uses the `Routes <http://routes.readthedocs.org/en/latest/>`_ python library for processing and mapping URLs. 

Defining Routes
---------------

URL routing is defined using functions. These functions accept a single argument, a *mapper object*. This mapper object has methods used to connect urls to behaviors, generate RESTful mappings and define *submappers* (described later). The mapping object has a few methods, the most important of which is ``connect``.

Traditionally the convention is for the mapper object (the argument to the function) to be named `urls` and the function to be named `map` but this is not strictly necessary. For more complex routing structures this convention can make reading the url map easier.

.. code-block:: python

    def map(urls):
        urls.connect('home', r'/', controller='home')

Once this function (or set of functions) is defined, it is passed into the Pybald Router when the router is initialized using the ``routes`` argument.

.. code-block:: python

    def map(urls):
        urls.connect('home', r'/', controller='home')

    app = Router(routes=map, controllers=[HomeController])

The router handles checking each request against the map, and when the path of a request is matched, will set a series of variables that will be used in routing and configuring the particular request.

Of the routing variables, the two most important are `controller` and `action`. These two variables, when set, will tell the Pybald router what code, which *handler*, will be executed when the match occurs. Handlers are generally methods on "controller" objects called "actions". Other variables can also be set, and those variables will be passed into the request to be processed.

.. note::

    The controller and action variables have default values. If no controller value is resolved, the value ``content`` will be used and if no action variable is passed, a default value of ``index`` will be used.


The ``connect`` method
~~~~~~~~~~~~~~~~~~~~~~

Lets assume you want to create a route for  showing blog posts. This url path might look something like `/blog/posts/45` to show a single blog post with an id, in this case 45. An example mapping function might look like the following:

.. code-block:: python

    def map(urls):
        urls.connect('home', r'/', controller='home')
        urls.connect('show_post', r'/blog/posts/{id}', controller='posts',
                     action='show')

Symbolic Names
**************
The first argument to the connect method is the symbolic name for the route. In this case the symbolic name is ``show_post``. The symbolic name for the route is used primarily for generating routes in templates and other places. Using a symbolic name for routes allows you to change the actual URL patterns that are being mapped at a later point and only have to change it in one place. By using meaninful symbolic names, you sepearate the URL paths from their application meaning, especially in templates where you might specify something like ``link('a good post').to('show_post')`` and not have to worry about the specific path that will be generated.

URL Path
********
The second argument to the connect method is the route itself, i.e. what path you wish to match on, in this case ``r'/blog/posts/{id}'``. This path has a *capture variable* that will be described later.

.. note::

    The ``r`` string format prefix is not necessary but useful since it tells python to interpret the string as a `'raw' python string <https://docs.python.org/2/reference/lexical_analysis.html#string-literals>`_ , where it will not interpret special characters or escape sequences (like backslashes, \\n will not create a newline but rather the two characters).

``controller`` and ``action`` Variables
***************************************
The controller and action variables are used to tell the pybald router which *handler* will be executed on a match. These can be set either by variable caprute or by setting them explicitly using keyword arguments.

The ``controller`` variable is used to look up which controller *object* will be instantiated to handle the request. The ``action`` variable is used to determine which method on the controller object will be executed. If no ``action`` argument is resolved, a default value of ``index`` will be used.

In the above example, controller and action are set explicitly using keyword arguments to `posts` and `show` respectively.

Conditions
**********
Conditions allow the restriction of the url match to more specific criteria. Generally conditions are used to restrict the URL match to specific HTTP methods or verbs (like GET, PUT and DELETE). They can also be used to match on specific subdomains or even custom matching functions.

.. code-block:: python

    def map(urls):
        urls.connect('home', r'/', controller='home')
        urls.connect('show_post', r'/blog/posts/{id}', controller='posts',
                     action='show', conditions={"method": ["GET", "HEAD"]})


Conditions are passed as a dictionary containing the condition key and data for each condition. In the above example, the ``show_post`` route will only match on ``GET`` and ``HEAD`` HTTP requests.

Additional Keyword Arguments
****************************
Lastly, any additional keyword variables can be set. These keyword arguments will be passed into the request.

Capturing Variables
~~~~~~~~~~~~~~~~~~~

In many cases it is useful to have a dynamic part of a URL that can be used in processing requests. In Pybald this is accomplished by using a *capture variable*, for example the {id} portion of the above route. By using these capture variables, you can extract information from the URL. In the following example the capture variable will set a value on a variable named `id` in the request and set it to any value present in the url. For example, with a request like `/blog/posts/45` the variable ``id`` will be set to 45 when the request is processed.

.. code-block:: pycon

    Route name Methods Path                
    home               /                   
    show_post          /blog/posts/{id}
    Welcome to the Pybald interactive console
     ** project: sample.py **
    >>> print c.get('/blog/posts/45')
    =============================== /blog/posts/45 ================================
    Method: GET
    action: show
    controller: posts
    id: 45
    200 OK
    Content-Type: text/html; charset=utf-8
    Content-Length: 12

    The id is 45

Variable Requirements
*********************

In the above example you may have noticed that this route match could potentially match on any value present on the url after `/blog/posts/`. If the request was `/blog/posts/frank`, the route would match and id would be `frank`. If, in your application, all ids are interger numbers, this might not be a case you want to have trigger your application behavior.

For this case you can use requirements in your variable captures. Requirements are regular expressions that can be used to limit what will be matched in the variable portion of your url route. Requirements use standard regular expressions and are added after a colon in the capture definition as follows:

.. code-block:: python

    def map(urls):
        urls.connect('home', r'/', controller='home')
        urls.connect('show_post', r'/blog/posts/{id:\d+}', controller='posts',
                     action='show')

Here we've added the requirement that there be one or more interger values after the url slash (and only interger values) to trigger the route match. This would match `/blog/posts/45` but not `/blog/posts/frank` or even `/blog/posts/45frank`.

.. code-block:: pycon

    Route name Methods Path                
    home               /                   
    show_post          /blog/posts/{id:\d+}
    Welcome to the Pybald interactive console
     ** project: sample.py **
     >>> c.get('/blog/posts/frank')
    ============================== /blog/posts/frank ==============================
    Method: GET
    HTTP Exception Thrown <class 'webob.exc.HTTPNotFound'>
    <Response at 0x7f1723c7ce10 404 Not Found>
    >>> c.get('/blog/posts/45frank')
    ============================= /blog/posts/45frank =============================
    Method: GET
    HTTP Exception Thrown <class 'webob.exc.HTTPNotFound'>
    <Response at 0x7f1723c7cd90 404 Not Found>
    >>> c.get('/blog/posts/45')
    =============================== /blog/posts/45 ================================
    Method: GET
    action: show
    controller: posts
    id: 45
    <Response at 0x7f1723c7ce50 200 OK>

.. note::

    In the preceding example, ErrorMiddleware has been added to make the listing clearer. Error handling will be covered later. Without  ErrorMiddleware, raw HTTP exceptions will be thrown on failed URL matches.

RESTful Resources
~~~~~~~~~~~~~~~~~

When creating CRUD applications, the routing layer of Pybald can automatically create a set of RESTful urls using the `collection` method on the mapper object.

This method creates a set of default action names based on common conventions for creating REST applications. It's still up to you to create action methods on your controller corresponding to the default names.

.. code-block:: python

    def map(urls):
        urls.connect('home', r'/', controller='home')
        urls.connect('show_post', r'/blog/posts/{id:\d+}', controller='posts',
                     action='show')
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

These follow some standard REST conventions (using PUT for updates, DELETE for deletes etc) while adding `new` and `edit` actions that are generally used to map to pages that display forms for creating new resources or editing existing resources.
