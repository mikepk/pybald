import sqlalchemy as sa
import sys
from pybald import context
import re

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
    )

import logging
log = logging.getLogger(__name__)

def create_engine():
    return sa.create_engine(context.config.database_engine_uri,
                                  **context.config.database_engine_args)


def create_dump_engine():
    '''Create a sql engine that just prints SQL using the current dialect to
    STDOUT instead of executing it.

    This is useful especially to see what the DDL statements are for various dialects
    '''
    def dump(sql, *multiparams, **params):
        sys.stdout.write( str(sql.compile(dialect=dump_engine.dialect) ).strip() +"\n")

    def dialect():
        match = re.search(r'^([^\:]*\:\/\/)', context.config.database_engine_uri)
        if match:
            return match.group(1)
        else:
            return "sqllite://"
    dump_engine = sa.create_engine(dialect(), strategy='mock', executor=dump)
    return dump_engine


def create_session(engine=None, session_args=None):
    # build session
    if session_args is None:
        session_args = {}
    session = scoped_session(sessionmaker(bind=engine, **session_args))
    return session