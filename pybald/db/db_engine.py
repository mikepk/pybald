import sqlalchemy as sa
import sys
from pybald import app

import logging
log = logging.getLogger(__name__)

engine_args = app.config.database_engine_args

if app.config.green:
    from SAGreen import green_connection, GreenThreadQueuePool
    engine_args["creator"] = green_connection()
    engine_args["poolclass"] = GreenThreadQueuePool


def dump(sql, *multiparams, **params):
    print str(sql.compile(dialect=dump_engine.dialect) )

# dump_engine = sa.create_engine('mysql://', strategy='mock', executor=dump)
dump_engine = sa.create_engine('postgresql://', strategy='mock', executor=dump)

try:
    engine = sa.create_engine(app.config.database_engine_uri, **engine_args)
except AttributeError:
    log.warning("**WARNING**\nSQLALchemy/pybald is using a mock"
                     " db connection.\n")
    engine = dump_engine

