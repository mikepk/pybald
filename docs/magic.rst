Magic
=====

Pybald only has a few 'magical' behaviors. This documentation explains how they work.


Loading Controllers
-------------------

Pybald relies on the use of convention over configuration. It assumes that a  project's files will be organized in a pre-defined way. Borrowing from Ruby on Rails, the main application lives under the ``./app`` path and application controllers are assumed to be stored in the project's ``./app/controllers`` path. Within this path, you can organize your controllers any way you wish, but generally the convention is to place one controller per module with a filename that matches the name of the contained controller. So, for example, a HomeController class may be located in a file named: ``./app/controllers/home_controller.py``.

It's also recommended that you follow the Python style guide (`PEP8 <http://www.python.org/dev/peps/pep-0008/>`_). Controller module (file) names are expected to be all lowercase, using underscores to separate words. Controller class names are expected to follow the CapWords convention.

On startup, when the pybald Router is first instantiated, but before the web application starts, the Router's ``load`` method is called. This method loads the app.controllers module.

The app.controllers package will scan the controllers path and look for classes that inherit from ``BaseController``. Any module that inherits from BaseController will be included in the package as well as the project's controller lookup table. The class name will be converted to underscore separated, lowercase text and the word "controller" will be stripped.

For example, to create a controller for blog post comments you might have a module like ``./app/controllers/post_comment_controller.py`` and a class defined like this:

.. code-block:: python

  from pybald.core.controller import BaseController

  class PostCommentController(BaseController):
      pass


This class would be loaded into the routers controller lookup table as 'post_comment'.

*How does this work?*

When the app.controllers package is loaded, a special ``pybald_class_loader`` function is called. This function recursively scans a path looking for classes that inherit from a pre-set list of target classes.

For controllers, the ``./app/controllers`` path is scanned with a list of ``(BaseController,)`` as the list of matching class names. Any module in the path that inherits from ``BaseController`` will be included in the list of exported classes. These are automatically pre-loaded into the package and exported in the ``__all__`` python 'magic method' of the package.

.. literalinclude:: /pybald_src/core/class_loader.py
   :pyobject: pybald_class_loader


Again taking cues from Ruby on Rails, the initial project is configured with a default route ``/{controller}/{action}/{id}``. This default route means that just by defining a new class, inheriting from ``BaseClass`` in the ``./app/controllers`` path, a URL will become immediately available at the 'lookup' value without any further configuration or additional route creation.

In the above example ``/post_comment`` would become available as a project route and the router would instantiate a PostCommentController object to handle the request.



The @action decorator
---------------------

Actions are any methods in Controllers with the exception of any methods whose name begins with an underscore. The standard pattern is to use the ``@action`` decorator to decorate each method you intend to use as an action. The ``@action`` decorator provides numerous convenience behaviors. A typical action will look like the following:

.. code-block:: python

  class HomeController(BaseController):
    '''A sample home controller'''
  
    @action
    def say_hello(self, req):
      return "hello world"


From the Router, each method is called with the WSGI call signature ``(environ, start_response)``. The action decorator uses the WSGI call to create a WebOb Request object which is passed to the method. Generally WebOb requests are easier and more convenient to deal with. The action decorator also provides three other convenience behaviors. 

The first is that it assigns to the controller instance, data that is parsed/processed per request (such as session, user, or url variables.) The second is that it processes the name of the controller/action and uses that to define a default template for this call. Lastly, the action decorator adds some intelligent behaviors for the return value of the action. If the action returns a string, the string will be wrapped in a Response object and returned. If the action returns a Response object directly, the action will return that. If the action returns nothing (or None) then an attempt will be made to render the expected template for this action.

.. literalinclude:: /pybald_src/core/controllers.py
   :pyobject: action



