import sqlalchemy as sa
import project
import sys

engine_args = project.database_engine_args

if project.green:
    from SAGreen import green_connection, GreenThreadQueuePool
    engine_args["creator"] = green_connection()
    engine_args["poolclass"] = GreenThreadQueuePool


def dump(sql, *multiparams, **params):
    print str(sql.compile(dialect=dump_engine.dialect) )

dump_engine = sa.create_engine('mysql://', strategy='mock', executor=dump)

try:
    engine = sa.create_engine(project.database_engine_uri, **engine_args)
except AttributeError:
    sys.stderr.write("**WARNING**\nSQLALchemy/pybald is using a mock"
                     " db connection.\n")
    engine = dump_engine

