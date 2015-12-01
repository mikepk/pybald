import sys
import re
import sqlalchemy as sa
from pybald import context

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
            return "sqlite://"
    dump_engine = sa.create_engine(dialect(), strategy='mock', executor=dump)
    return dump_engine