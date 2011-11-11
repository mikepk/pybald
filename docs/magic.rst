Magic
=====

PyBald only has a few 'magical' behaviors. This documentation explains how they work.


Loading Controllers
-------------------

PyBald uses the idea of convention over configuration. It assumes that a PyBald project's files will be organized in a specific way. Borrowing from Ruby on Rails, application controllers are assumed to be stored, one per file, in the project's ``./app/controllers`` directory. Each controller also follows the name convention of **name**\_controller.py. So, for example, a controller named ``hello`` would be in a file named ``hello_controller.py`` inside the directory ``./app/controllers``. Following proper Python styles, the controller is then declared with the same name but in CamelCase inside this file. The translation is underscores in the file names will be converted to CamelCase when looking for the class in the file.

.. code-block:: python

  class HomeController(BaseController):
      pass

There's no requirement that this be the *only* class in the file, you can have as many classes in these files as you wish, but only the class name mapping to the file name will be used for controllers.

When the Router is first created, but before the web application starts, the Router's ``load`` method is called. This method scans the ``./app/controllers`` directory and loads all of the controller modules into the Router object. 

Again taking cues from Ruby on Rails, the project is configured with a default route ``/{controller}/{action}/{id}``. This default route means that just by creating a new **name**\_controller.py file in the ./app/controllers project directory, the URL will become immediately available without any further configuration or additional route creation.

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

Actions are any methods in Controllers that do not begin with an underscore. The standard pattern is to use the ``@action`` decorator to decorate each method you intend to use as an action. The ``@action`` decorator provides numerous convenience behaviors. A typical action will look like the following:

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
  # This decorator takes in the action method and adds some syntactic sugar around it.
  # Allows the actions to work with WebOb request / response objects, and handles default
  # behaviors, such as displaying the view when nothing is returned, or plain text
  # if a string is returned.
  def action(func):
      def replacement(self, environ, start_response):
          req = Request(environ)
          # this code defines the template id to match against
          # template path = controller name + '/' + action name (except in the case of)
          # index
          self.template_id = re.search('(\w+)Controller',self.__module__).group(1).lower()
          # 'index' is a special name. The index action maps to the controller name (no action view)
          if not re.search('index',func.__name__):
              self.template_id += '/'+str(func.__name__)

          # add any url variables as members of the controller
          if req.urlvars:
              ignore = ['controller','action']
              for key in req.urlvars.keys(): # and not in ignore:
                  #Set the controller object to contain the url variables
                  # parsed from the dispatcher / router
                  setattr(self,key,req.urlvars[key])

          # run the controllers "pre" code
          resp = self._pre(req)
          # If the pre code returned a response, return that
          if not resp:
              try:
                  resp = func(self,req)
              except exc.HTTPException, e:
                  resp = e

          # if there's no return, call the view method
          if not resp:
              resp = self._view()

          # if the function returns a string
          # wrap it in a response object
          if isinstance(resp, basestring):
              resp = Response(body=resp)

          # run the controllers post code
          self._post(req,resp)

          return resp(environ, start_response)
      return replacement

The action decorator provides four "magical" behaviors. 

1. The first is that it encapsulates the action with a function that accepts the normal WSGI pattern ``(environ,start_response)`` (line 7). Then it calls the action with a WebOb Request (line 30). 
2. It uses the controller and action/method name to determine the name of the template to render (lines 12-15).
3. It assigns any url variables parsed by the Routes module to the controller object (lines 17-23).
4. Lastly if the action returns nothing, it tries to invoke the template engine (line 36) or if it returns a plain string it wraps the string in a Response object (lines 40-41)


