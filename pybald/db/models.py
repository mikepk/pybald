
from sqlalchemy import (
    MetaData, 
    INT as Int,
    Integer,
    Float,
    Column, 
    ForeignKey, 
    String, 
    DateTime, 
    TIMESTAMP as TimeStamp, 
    PickleType,
    Time,
    Table,
    or_,
    and_,
    not_,
    select
    )

from sqlalchemy.types import (
    BLOB,
    BOOLEAN,
    BigInteger,
    Binary,
    Boolean,
    CHAR,
    CLOB,
    DATE,
    DATETIME,
    DECIMAL,
    Date,
    DateTime,
    Enum,
    FLOAT,
    Float,
    INT,
    INTEGER,
    Integer,
    Interval,
    LargeBinary,
    NCHAR,
    NVARCHAR,
    NUMERIC,
    Numeric,
    PickleType,
    SMALLINT,
    SmallInteger,
    String,
    TEXT,
    TIME,
    TIMESTAMP,
    Text,
    Time,
    Unicode,
    UnicodeText,
    VARCHAR,
    )


from sqlalchemy.orm import (
    column_property,
    mapper, 
    scoped_session, 
    sessionmaker, 
    reconstructor,
    relationship, 
    backref, 
    contains_eager,
    eagerload, 
    eagerload_all,
    joinedload,
    synonym
    )

from sqlalchemy.orm.exc import (
    NoResultFound, 
    MultipleResultsFound
    )

from sqlalchemy.sql import (
    exists,
    )

from sqlalchemy.sql.expression import (
    asc,
    desc,
    )

from sqlalchemy import func

import re
from pybald.db.db_engine import engine

from pybald.util import camel_to_underscore, pluralize

# for green operation
import project
if project.green:
    from SAGreen import eventlet_greenthread_scope
    session = scoped_session(sessionmaker(bind=engine), scopefunc=eventlet_greenthread_scope)
else:
    session = scoped_session(sessionmaker(bind=engine))


import sqlalchemy.ext.declarative
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(bind=engine)


class NotFound(NoResultFound):
    '''Generic Not Found Error'''
    pass

class ModelMeta(sqlalchemy.ext.declarative.DeclarativeMeta):
    def __init__(cls, name, bases, ns):
        try:
            if Model not in bases:
                return
        except NameError:
            return
        # set the tablename, if it's user set, use that, otherwise use a function to create one
        cls.__tablename__ = getattr(cls, "__tablename__" , pluralize( camel_to_underscore(name) )) 
        # tableargs adds autoload to create schema reflection
        cls.__table_args__ = getattr(cls, "__table_args__", {})
        if project.schema_reflection:
            # create or update the __table_args__ attribute
            cls.__table_args__['autoload'] = True
        if project.global_table_args:
            cls.__table_args__.update(project.global_table_args)

        super(ModelMeta, cls).__init__(name, bases, ns)


class ModelApi(Base):
    '''Pybald Model class, inherits from SQLAlchemy Declarative Base.'''
    __metaclass__ = ModelMeta
    

    
    def save(self, commit=False):
        '''Save this instance. 
        
        When commit is False, stages data for later commit.
        '''
        
        session.add(self)
        
        if commit:
            self.flush()
        return self

    def delete(self, commit=False):
        '''Delete this instance.'''
        session.delete(self)
        if commit:
            self.flush()
        return self


    def flush(self):
        '''Call the commit for the entire session (includes anything else pending)'''
        session.flush()
        return self


    def commit(self):
        '''Call the commit for the entire session (includes anything else pending)'''
        session.commit()
        return self

    @classmethod
    def get(cls,**where):
        '''Construct a load query with keyword arguments as the filter argument and return the instance.'''
        return cls.load(**where).one()

    @classmethod
    def all(cls,**where):
        '''Returns a list of objects that can be qualified. all() without arguments returns all the items of the model type.'''
        return cls.load(**where).all()

    # methods that return queries (must execute to retrieve)
    # =============================================================
    @classmethod
    def load(cls,**where):
        '''Build a sqlalchemy load query to return stored objects. 
        
        Returns a query object that must execute the query to retrieve.
        '''
        if where:
            return session.query(cls).filter_by(**where)
        else:
            return session.query(cls)

    @classmethod
    def query(cls):
        '''Simple Query method based on the class.'''
        return session.query(cls)


    @classmethod
    def all(cls,**where):
        '''Returns a list of objects that can be qualified. all() without arguments returns all the items of the model type.'''
        return cls.load(**where).all()


class RoModel(object):
    '''Read only version of the Model class.'''

    @classmethod
    def protect(cls, protect=True):
        cls.__bases__ = (ModelApi,)


class Model(ModelApi):
    NotFound = sqlalchemy.orm.exc.NoResultFound

    id = Column(Integer, nullable=False, primary_key=True)

    @classmethod
    def protect(cls, protect=True):
        if protect:
            cls.__bases__ = (RoModel,)
        else:
            cls.__bases__ = (ModelApi,)