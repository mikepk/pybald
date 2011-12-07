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

.. code-block:: python

  from pybald.util import underscore_to_camel

  __all__ = []
  def load_controllers():
      for modulefile in glob.iglob( os.path.join(__path__[0],
                                                 "*_controller.py") ):
          modname = re.search('(\w+_controller)\.py',modulefile).group(1)
          imp_modname = 'app.controllers.'+modname
          class_name = underscore_to_camel(modname)
          # print modname, class_name
          temp = __import__(modname, globals(), locals(), [modname], 1)
          __all__.append(modname)
  load_controllers()

  
1. First the controllers path is scanned with the glob module for the pattern ``*.Controllers.py`` (line 4).
2. The module name is extracted *Name*\ Controller (minus the file extension) as *modname* (line 5).
3. The *import* module name is the full qualified name. Thats ``app.controllers.``\ +\ *modname* is stored is *imp_modname* (line 6).
4. The *Name* portion is stored as the default controller name for URL mapping. (lines 10-11)
5. The \_\_import\_\_ function is used to load each of the controllers modules into the Router object and store the controllers modules in the Router associated with their name. (lines 17-23).
6. Calls **Route's** ``create_regs`` method to create regular expressions for mapping to the controller names.

The @action decorator
---------------------

Actions are any methods in Controllers with the exception of any methods whose name begins with an underscore. The standard pattern is to use the ``@action`` decorator to decorate each method you intend to use as an action. The ``@action`` decorator provides numerous convenience behaviors. A typical action will look like the following:

.. code-block:: python

  class HomeController(BaseController):
    '''A sample home controller'''
  
    @action
    def say_hello(self, req):
      return "hello world"


From the Router, each method is called with the WSGI pattern ``(environ, start_response)``. The action decorator uses the WSGI call to create a WebOb Request object which is passed to the method. Generally WebOb requests are easier and more convenient to deal with. The action decorator also provides three other convenience behaviors. 

The first is that it assigns to the controller instance, data that is parsed/processed per request (such as session, user, or url variables.) The second is that it processes the name of the controller/action and uses that to define a default template for this call. Lastly, the action decorator adds some intelligent behaviors for the return value of the action. If the action returns a string, the string will be wrapped in a Response object and returned. If the action returns a Response object directly, the action will return that. If the action returns nothing (or None) then an attempt will be made to render the expected template for this action.



.. code-block:: python

    # action / method decorator
    def action(method):
        '''
        Decorates methods that are WSGI apps to turn them into pybald-style actions.

        :param method: A method to turn into a pybald-style action.

        This decorator is usually used to take the method of a controller instance 
        and add some syntactic sugar around it to allow the method to use WebOb
        Request and Response objects. It will work with any method that 
        implements the WSGI spec.
    
        It allows actions to work with WebOb request / response objects and handles
        default behaviors, such as displaying the view when nothing is returned, 
        or setting up a plain text Response if a string is returned. It also 
        assigns instance variables from the ``pybald.extension`` environ variables
        that can be set from other parts of the WSGI pipeline.
    
        This decorator is optional but recommended for making working
        with requests and responses easier.
        '''
        @wraps(method)
        def action_wrapper(self, environ, start_response):
            req = Request(environ)

            # add any url variables as members of the controller
            for key in req.urlvars.keys():
                #Set the controller object to contain the url variables
                # parsed from the dispatcher / router
                setattr(self, key, req.urlvars[key])

            # this code defines the template id to match against
            # template path = controller name + '/' + action name (except in the case of)
            # index
            if not hasattr(self, "template_id"):
                if method.__name__ not in ('index','__call__'):
                    self.template_id = "{0}/{1}".format(camel_to_underscore(
                             self.controller_pattern.search(self.__class__.__name__
                                                      ).group(1)), method.__name__)
                else:
                    self.template_id = camel_to_underscore(
                             self.controller_pattern.search(self.__class__.__name__
                                                      ).group(1))

            # add the pybald extension dict to the controller
            # object
            extension = req.environ.get('pybald.extension', None)
            if extension:
                for key, value in extension.items():
                    setattr(self, key, value)

            # Return either the controllers _pre code, whatever
            # is returned from the controller
            # or the view. So pre has precedence over
            # the return which has precedence over the view
            resp = self._pre(req) or method(self, req) or self._view()

            # if the response is currently a string
            # wrap it in a response object
            if isinstance(resp, basestring):
                resp = Response(body=resp, charset="utf-8")

            # run the controllers post code
            self._post(req, resp)

            return resp(environ, start_response)
        return action_wrapper


The action decorator provides four "magical" behaviors. 

1. The first is that it encapsulates the action with a function that accepts the normal WSGI pattern ``(environ,start_response)`` (line 7). Then it calls the action with a WebOb Request (line 30). 
2. It uses the controller and action/method name to determine the name of the template to render (lines 12-15).
3. It assigns any url variables parsed by the Routes module to the controller object (lines 17-23).
4. Lastly if the action returns nothing, it tries to invoke the template engine (line 36) or if it returns a plain string it wraps the string in a Response object (lines 40-41)


