from sqlalchemy.interfaces import ConnectionProxy

# A simple way to wrap database transactions in either a query timer.
# or more interestingly an instrumented stack tracer that annotates
# queries with the calling function. Allows the MySQL slow query log
# to be uesed to find what code is issuing slow queries.

# import time
# import logging

# logging.basicConfig()
# logger = logging.getLogger("myapp.sqltime")
# logger.setLevel(logging.DEBUG)

class InstrumentedProxy(ConnectionProxy):
    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
        try:
            import inspect
            stack = inspect.stack()
            # get the calling frame for the method/function calling
            # the sql command (taking into account the sql+execute functions)
            max_stack = len(stack) - 1
            print max_stack
            try:
                # for f in stack:
                #     frame = f[0]
                #     frame_info = inspect.getframeinfo(frame)
                #     debug = 'method:'+str(frame_info[2])+' file:'+str(frame_info[0])+' line:'+str(frame_info[1])
                #     print stack.index(f), debug

                frame = stack[14][0]
                frame_info = inspect.getframeinfo(frame)

                debug = 'method:'+str(frame_info[2])+' file:'+str(frame_info[0])+' line:'+str(frame_info[1])
                statement += ' -- '+debug
            except IndexError:
                pass
            return execute(cursor, statement, parameters, context)
        except:
            pass

# use by passing the proxy to the engine
#engine = sa.create_engine(project.get_engine(), proxy=InstrumentedProxy(), **engine_args)