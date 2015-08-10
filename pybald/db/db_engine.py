import sqlalchemy as sa
import sys
from pybald import app
import re

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

import logging
log = logging.getLogger(__name__)

def connect_database():
    engine_args = app.config.database_engine_args

    if app.config.green:
        from SAGreen import green_connection, GreenThreadQueuePool
        engine_args["creator"] = green_connection()
        engine_args["poolclass"] = GreenThreadQueuePool


    def dump(sql, *multiparams, **params):
        sys.stdout.write( str(sql.compile(dialect=dump_engine.dialect) ).strip() +"\n")

    def dialect():
        match = re.search(r'^([^\:]*\:\/\/)', app.config.database_engine_uri)
        if match:
            return match.group(1)
        else:
            return "mysql://"

    dump_engine = sa.create_engine(dialect(), strategy='mock', executor=dump)

    try:
        engine = sa.create_engine(app.config.database_engine_uri,
                                  **app.config.database_engine_args)
    except AttributeError:
        log.warning("**WARNING**\nSQLALchemy/pybald is using a mock"
                         " db connection.\n")
        engine = dump_engine

    # build session
    session_args = {}

    if app.config.green:
        from SAGreen import eventlet_greenthread_scope
        session_args['scopefunc'] = eventlet_greenthread_scope

    session = scoped_session(sessionmaker(bind=engine, **session_args))
    return session