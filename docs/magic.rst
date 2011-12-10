Magic
=====

Pybald only has a few 'magical' behaviors. This documentation explains how they work.


Loading Controllers
-------------------

Pybald uses the idea of convention over configuration. It assumes that a  project's files will be organized in a specific way. Borrowing from Ruby on Rails, application controllers are assumed to be stored, one per file, in the project's ``./app/controllers`` directory. Each controller also follows the name convention of **name**\_controller.py. So, for example, ``./app/controllers/hello_controller.py``. 

Following the Python style guide (`PEP8 <http://www.python.org/dev/peps/pep-0008/>`_), controller module names are expected to be all lowercase, using underscores to separate words. Inside the module the controller class is declared with the same name converted to CamelCase. For example, to create a controller for blog posts you might have a module like ``./app/controllers/post_controller.py`` and the class would look something like this:

.. code-block:: python

  from pybald.core.controller import BaseController

  class PostController(BaseController):
      pass

While Pybald will look for this name correspondence, there's no requirement that this be the *only* class in the file. You can have as many classes in these files as you wish, but only the class name mapping to the file name will be automatically used for controllers.

When the Router is first created, but before the web application starts, the Router's ``load`` method is called. This method scans the ``./app/controllers`` directory and loads all of the controller modules it finds into the Router object. 

Again taking cues from Ruby on Rails, the initial project tempalte is configured with a default route ``/{controller}/{action}/{id}``. This default route means that just by creating a new **name**\_controller.py file in the ./app/controllers project directory, the URL will become immediately available without any further configuration or additional route creation.

.. literalinclude:: /pybald_src/project_template/app/controllers/__init__.py
  
1. First the controllers path is scanned with the glob module for the pattern ``*.Controllers.py`` 
2. The module name is extracted *Name*\ Controller (minus the file extension) as *modname* .
3. The *import* module name is the full qualified name. Thats ``app.controllers.``\ +\ *modname* is stored is *imp_modname* .
4. The *Name* portion is stored as the default controller name for URL mapping. 
5. The ``__import__`` function is used to load each of the controllers modules into and adds them to the controllers namespace under ``__all__``.
6. The Router component will load all controllers from app.controllers.


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



