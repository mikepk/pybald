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
    sys.stdout.write( str(sql.compile(dialect=dump_engine.dialect) ).strip() +"\n")


import re
def dialect():
    match = re.search(r'^([^\:]*\:\/\/)', app.config.database_engine_uri)
    if match:
        return match.group(1)
    else:
        return "mysql://"

dump_engine = sa.create_engine(dialect(), strategy='mock', executor=dump)

try:
    engine = sa.create_engine(app.config.database_engine_uri, **app.config.database_engine_args)
except AttributeError:
    log.warning("**WARNING**\nSQLALchemy/pybald is using a mock"
                     " db connection.\n")
    engine = dump_engine

