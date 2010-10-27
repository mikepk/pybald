#!/usr/bin/env python
# encoding: utf-8
"""
SAGreen.py

Support code to allow SQLalchemy to operate correctly with Eventlet and Green Threads.

Created by mikepk on 2010-10-15.
Copyright (c) 2010 Michael Kowalchik. All rights reserved.
"""

import sqlalchemy.engine.url
from sqlalchemy.pool import QueuePool

from eventlet import timeout

import project
import eventlet

import os
os.environ["EVENTLET_THREADPOOL_SIZE"] = "20"
# importing tpool automatically spawns 20 native threads
# tunable with an env variable
from eventlet import tpool

class ConnectTimeout(Exception):
    '''Connection timeout.'''
    pass

def eventlet_greenthread_scope():
    '''Greenthread scope function for sqlalchemy scoped sessions.'''
    return id(eventlet.greenthread.getcurrent())

class GreenThreadQueuePool(QueuePool):
    '''Simple subclass of the standard SA QueuePool. Uses a sleep when the pool is empty to green thread switch.'''
    def do_get(self):
        # while the queue pool is filled, switch to another thread until one is available
        # TODO: Add timeout code to make sure this doesn't spin forever and deadlock
        # if something goes wrong in the db connections
        while self._max_overflow > -1 and self._overflow >= self._max_overflow:
            eventlet.sleep(0)
        return super(GreenThreadQueuePool,self).do_get()


# lifting some of the logic from sqlalchemy
# to reuse the dialect / url parsing to create
# connection arguments
def convert_url_to_connection_args(name_or_url, **kwargs):
    url = sqlalchemy.engine.url.make_url(name_or_url)
    dialect_cls = url.get_dialect()

    # get the correct DBAPI base on connection url
    dbapi_args = {}
    dbapi = dialect_cls.dbapi(**dbapi_args)

    # create the dialect
    dialect_args = {'dbapi':dbapi}
    dialect = dialect_cls(**dialect_args)

    # assemble connection arguments
    # for this dialect
    (cargs, connection_params) = dialect.create_connect_args(url)
    return dbapi, connection_params


def green_connection():
    '''Create a green databse connection.'''    
    dbapi, kw = convert_url_to_connection_args(project.get_engine())
    # TODO: this should check for supported dbapis before proceeding

    def eventlet_connection_creator():
        '''Creator method to wrap DBAPI connections with native threads to allow non-blocking db access.'''
        # This code is lifted and slightly tweaked 
        # from the db_pool in the eventlet package
        t = timeout.Timeout(20, ConnectTimeout())
        try:
            conn = dbapi.connect(**kw)
            ## I think this is to keep the connection itself from blocking
            ## unfortunately it's hanging. The proxied connection still works
            ## nonblockingly though.
            # conn = tpool.execute(dbapi.connect, **kw)
            proxied_connection = tpool.Proxy(conn, autowrap_names=('cursor',))
            return proxied_connection
        finally:
            # cancel the timeout
            t.cancel()  

    return eventlet_connection_creator
