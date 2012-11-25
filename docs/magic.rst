Magic
=====

Pybald only has a few 'magical' behaviors. This documentation explains how they work.


Loading Controllers
-------------------

Pybald uses the idea of convention over configuration. It assumes that a  project's files will be organized in a specific way. Borrowing from Ruby on Rails, application controllers are assumed to be stored in the project's ``./app/controllers`` directory. Within this path, you can organize your controllers any way you wish, but generally the convention is to place one controller per module with a filename that matches the name of the contained controller. So, for example, a HomeController class may be located in a file named: ``./app/controllers/hello_controller.py``.

It's also recommended that you follow the Python style guide (`PEP8 <http://www.python.org/dev/peps/pep-0008/>`_), controller module names are expected to be all lowercase, using underscores to separate words. Controller class names are expected to follow the  CapWords convention.

The only magic is that, on startup, the pybald router will scan the controllers path and look for classes that inherit from ``BaseController``. Any module that inherits from BaseController will be included in the projects lookup table. The class name will be converted to underscore separated, lowercase and the word "controller" is stripped. 

For example, to create a controller for blog posts you might have a module like ``./app/controllers/post_controller.py`` and the class would look something like this:

.. code-block:: python

  from pybald.core.controller import BaseController

  class PostController(BaseController):
      pass


When the app.controllers module is loaded, a special ``pybald_class_loader`` function is called. This function scans a path looking for classes that inherit from a list of passed in classes. For controllers, the ``./app/controllers`` path is passed in with a list of ``(BaseController,)`` as the list of matching class names. Any module in the path that inherits from ``BaseController`` will be included in the list of exported classes.

.. literalinclude:: /pybald_src/core/__init__.py
   :pyobject: pybald_class_loader

When the Router is first created, but before the web application starts, the Router's ``load`` method is called. This method scans the ``./app/controllers`` directory and loads all of the controller modules it finds into the Router object. 



Again taking cues from Ruby on Rails, the initial project tempalte is configured with a default route ``/{controller}/{action}/{id}``. This default route means that just by creating a new **name**\_controller.py file in the ./app/controllers project directory, the URL will become immediately available without any further configuration or additional route creation.



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



