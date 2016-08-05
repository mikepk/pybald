Templates
=========

The pybald web framework uses Mako templates by default for rendering content.

Setting up templates
--------------------

Pybald is configured to use mako template files. By default, the ``template_path`` is defined as ``app/views``. We're going to override the default path that pybald normally looks for template files for our simple example app. Let's update our small example pybald app to include the ``template_path`` configuration directive and set it to the root path of the project.


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

