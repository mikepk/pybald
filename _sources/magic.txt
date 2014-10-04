Magic
=====

Pybald only has a few 'magical' behaviors. This documentation explains how they work.


Loading Controllers
-------------------

Pybald uses a 'controller registry' for keeping track of which classes are to be used as controllers. This registry is just a list of all controllers that have been imported / loaded in the current project. To register a class to act as a controller, you can inherit from the pybald.core.Controller class. Inheriting from this class will automatically register the class as a controller.

.. code-block:: pycon

  >>> from pybald.core.controllers import Controller
  >>> class PostCommentController(Controller):
  ...    pass
  ... 
  >>> print Controller.registry
  [<class '__main__.PostCommentController'>]


While you can organize your controller classes any way you wish, the convention is to place one controller per module with a filename that matches the name of the contained controller. So, for example, a HomeController class might be located in a file named: ``./app/controllers/home_controller.py``. Additionally, for a controller to be registered, its class must be defined and/or its containing module imported. There are some convenience utilities for auto-importing entire paths which will be discussed later.

It's also recommended that you follow the Python style guide (`PEP8 <http://www.python.org/dev/peps/pep-0008/>`_). Controller module (file) names are expected to be all lowercase, using underscores to separate words. Controller class names are expected to follow the CapWords convention.

On startup, when the pybald Router is first instantiated, but before the web application starts, the Router is passed a controller registry to use for associating with the route map.

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



