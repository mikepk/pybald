
from newrelic.agent import (current_transaction, wrap_function_wrapper,
                           FunctionTrace, WSGIApplicationWrapper)
from newrelic.api.function_trace import FunctionTraceWrapper
from functools import wraps, partial
import logging
console = logging.getLogger(__name__)

# define a new_relic_trace_wsgi function
nr_trace_wsgi = partial(FunctionTraceWrapper, group="Python/Pybald/WSGI")


class NewrelicPybald(object):
    '''
    Just a passthrough to remove the extra function definition from Newrelic
    when it instruments WSGI apps.

    This is a hack just for formatting purposes. It adds a layer to the WSGI
    stack which is a little non-ideal but avoids having to fork/hack newrelic's
    code.
    '''
    def __init__(self, application, name=None):
        if name:
            self.__class__.__name__ = name
        self.application = application

    def __call__(self, *args, **kargs):
        return self.application(*args, **kargs)


def handler_wrapper(name):
    def _inner_wrap(method):
        @wraps(method)
        def _wrapper(*args, **kargs):
            transaction = current_transaction()
            if transaction is None:
                return method(*args, **kargs)
            # name = "{0}:{1}".format(controller_name, action_name)
            # name = callable_name(wrapped)
            # console.debug(name)
            transaction.set_transaction_name(name)
            with FunctionTrace(transaction, name, group="Python"):
                return method(*args, **kargs)
        return _wrapper
    return _inner_wrap


def wrapper_Pybald_Router_get_handler(wrapped, instance, args, kwargs):
    '''
    Wrap the Pybald router's 'get handler' method with a function to
    automatically set the transaction name to the pybald contoller/action
    id.

    Monkeypatches the Router and allows us to dynamically wrap the return
    handler action on return.
    '''
    action = wrapped(*args, **kwargs)
    action_name = action.__name__

    # Get the classname of the containing instance (if applicable)
    controller_classname = ""
    if hasattr(action, '__self__'):
        controller = action.__self__
        if hasattr(controller, '__class__'):
            controller_classname = controller.__class__.__name__

    name = "{0}:{1}".format(controller_classname, action_name)
    #console.debug("Wrapped router action name: {}".format(name))
    action = handler_wrapper(name)(action)
    return action


def add_wsgi_trace(app):
    '''Recursively walk the WSGI stack adding new relic trace wrappers.

    :param app: A WSGI application to apply newrelic instrumentation to
    '''
    try:
        next_level = app.application
        if next_level is None:
            return True
        else:
            app.application = nr_trace_wsgi(next_level)
    except AttributeError:
        return True
    return add_wsgi_trace(next_level)


def instrument_pybald(app, name=None):
    '''
    Add the WSGI Transaction wrapper for newrelic.

    Also recursively walks
    up the WSGI stack and adds FunctionTraceWrappers to all of the WSGI apps
    above the instrumentation point.

    :param app: A WSGI application to apply newrelic instrumentation to
    :param name: The (optional) name of the application
    '''
    import pybald
    app = NewrelicPybald(app, name)
    add_wsgi_trace(app)
    app = WSGIApplicationWrapper(app, name=name, group="Python",
                                 framework=("Pybald", pybald.__version__))
    return app


def instrument_pybald_app(app, name=None):
    '''
    Monkeypatch the Pybald Router and instrument the WSGI stack with
    FunctionTrace wrappers.

    This allows the breakdown of all of the components in the Pybald stack and
    also sets the transaction names to the controller/action pairs for
    user code.

    :param app: A WSGI application to apply newrelic instrumentation to
    :param name: The (optional) name of the application
    '''
    import pybald.core.router
    wrap_function_wrapper(pybald.core.router, 'Router.get_handler',
                          wrapper_Pybald_Router_get_handler)
    return instrument_pybald(app, name=name)
