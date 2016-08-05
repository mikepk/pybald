Templates
=========

The pybald web framework uses Mako templates by default for rendering content.

Setting up templates
--------------------

.. sidebar:: Why ``app/views``?

    While pybald is generally designed to be quick to start and play with, it also tries to help you be ready for when your project grows. Pybald encourages a particular application path structure to help you stay organized longer term. In general application code is encouraged to be put in ``app/`` with the subfolders of ``app/models``, ``app/views`` and ``app/controllers``. Pybald is also designed to be flexible, so we're ignoring that structure for our simple example.

Pybald uses mako template files. By default, the ``template_path`` is defined as ``app/views``. We're going to override the default path that pybald normally looks for template files for our simple example app. Let's update our small example pybald app to include the ``template_path`` configuration directive and set it to the root path of the project. Where we call ``pybald.configure`` we'll add ``template_path="."``.


.. code-block:: python

    # configure our pybald application
    pybald.configure(debug=True, template_path=".")

Once we've done this, pybald will know to look for template files in the same path as the root application.

Your first template
-------------------

Lets create a template file and call it ``home.html.template``. This will be an html template to generate content for our application. In this file, lets add the following content and save the file. This isn't terribly exciting for now, but we'll show more of the power of templates later.

.. code-block:: html

    <html>
    <head></head>
    <body>
        <h1>Hello world!</h1>
    </body>
    </html>

Now let's render this template. Let's go ahead and start up our console again using ``python sample.py console``. We'll import the pybald *context* and then use the ``render`` function in the current context. 

.. code-block:: pycon

    Route name Methods Path
    home               /   
    Welcome to the Pybald interactive console
     ** project: sample.py **
    >>> from pybald import context
    >>> content = context.render("home.html.template")
    Using template: home.html.template
    Rendering template
    >>>
    >>> print content
    <html>
    <head></head>
    <body>
    <h1>Hello world!</h1>
    </body>
    </html>

We've just rendered a simple template to a string.

The reason we use the context is because the template system needs to have a certain amount of configuration to run correctly and the context represents the current configuration. For example, the template system needs to know where to look for the template files and what template filters to apply (described later).

Using the template in a request
-------------------------------

We've just rendered a template, but we got a string value back, how do we use the results in our web requests? The answer is simple: we just return that string from one of our *actions*.

We can update our sample application to return the rendered template.

.. code-block:: python

    import pybald
    from pybald import context
    from pybald.core.controllers import Controller, action
    from pybald.core.router import Router

    # configure our pybald application
    pybald.configure(debug=True, template_path=".")

    def map(urls):
        urls.connect('home', r'/', controller='home')

    class HomeController(Controller):
        @action
        def index(self, req):
            return context.render("home")

    # this is the WSGI pipeline
    app = Router(routes=map, controllers=Controller.registry)

    if __name__ == "__main__":
        context.start(app)

Now we can run our application and initiate a simulated web request as before, only this time we'll return the results of a template render.

.. code-block:: pycon

    Route name Methods Path
    home               /   
    Welcome to the Pybald interactive console
     ** project: sample.py **
    >>> resp = c.get("/")
    ====================================== / ======================================
    Method: GET
    action: index
    controller: home
    Using template: /home.html.template
    Rendering template
    >>> print resp
    200 OK
    Content-Type: text/html; charset=utf-8
    Content-Length: 65

    <html>
    <head></head>
    <body>
    <h1>Hello world!</h1>
    </body>
    </html>


You'll notice that in this example we've just used ``"home"`` for the argument to ``context.render``. This is one of the conveinience behaviors of pybald, the default file extension for html templates is ``.html.template`` so you don't have to explicitly use the full filename.

Using data in templates
-----------------------

Now lets do something interesting with the template. Templates allow us to bind data to them and use them to create variables and execute template logic.

First lets update the template to create a placeholder, a variable.

..code-block:: html

    <html>
    <head></head>
    <body>
    <h1>Hello world!</h1>
    <h2>Greetings to ${name}</h2>
    </body>
    </html>