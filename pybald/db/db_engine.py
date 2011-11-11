import sqlalchemy as sa
import project

engine_args = project.database_engine_args

if project.green:
    from SAGreen import green_connection, GreenThreadQueuePool
    engine_args["creator"] = green_connection()
    engine_args["poolclass"] = GreenThreadQueuePool

engine = sa.create_engine(project.database_engine_uri, **engine_args)


def dump(sql, *multiparams, **params):
    print str(sql.compile(dialect=dump_engine.dialect) )

dump_engine = sa.create_engine('mysql://', strategy='mock', executor=dump)