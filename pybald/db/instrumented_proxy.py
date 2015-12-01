from sqlalchemy.interfaces import ConnectionProxy

# A simple way to wrap database transactions in either a query timer.
# or more interestingly an instrumented stack tracer that annotates
# queries with the calling function. Allows the MySQL slow query log
# to be uesed to find what code is issuing slow queries.

class InstrumentedProxy(ConnectionProxy):
    '''A proxy to the underlying SQL execution engine.

    This proxy intercepts sql calls and allows timing and/or annotation
    of the SQL. With annotation, allows interesting patterns like using the
    database logging facilities to log slow queries and find what code
    is actually triggering the SQL by seeing the comment / annotation of
    the executed SQL statement.

    use by passing the proxy to the engine
    > engine = sa.create_engine(project.database_engine_uri, proxy=InstrumentedProxy(), **engine_args)
    '''
    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
        '''The cursor execution proxy.

        This is the code that actually runs before running the underlying sql
        engine. In this case, attempts to walk up the current executing
        stack to find the code that triggered this query.
        '''
        try:
            import inspect
            stack = inspect.stack()
            # get the calling frame for the method/function calling
            # the sql command (taking into account the sql+execute functions)
            # max_stack = len(stack) - 1
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

