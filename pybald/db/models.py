
from pybald.db.db_engine import engine

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
    Table
    )

from sqlalchemy.orm import (
    mapper, 
    scoped_session, 
    sessionmaker, 
    reconstructor
    )
    
from sqlalchemy.orm import (
    relationship, 
    backref, 
    eagerload, 
    eagerload_all
    )

from sqlalchemy.orm.exc import (
    NoResultFound, 
    MultipleResultsFound
    )



import re

# for green operation
import project
if project.green:
    from SAGreen import eventlet_greenthread_scope
    db = scoped_session(sessionmaker(bind=engine), scopefunc=eventlet_greenthread_scope)
else:
    db = scoped_session(sessionmaker(bind=engine))

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(bind=engine)


class NotFound(NoResultFound):
    '''Generic Not Found Error'''
    pass

class Plural(object):
    '''Simple Pluralizer object. Stores naive rules for word pluralization.'''
    def buildRule(self, (pattern, search, replace)):                                        
        return lambda word: re.search(pattern, word) and re.sub(search, replace, word)

    def __init__(self):
        '''Init pluralizer'''
        #Build regex patterns to do a quick and dirty pluralization.
        self.patterns = [['[^aeiouz]z$', '$', 's'], 
                         ['[aeiou]z$', '$', 'zes'], 
                         ['[sx]$', '$', 'es'], 
                         ['[^aeioudgkprt]h$', '$', 'es'], 
                         ['[^aeiou]y$', 'y$', 'ies'], 
                         ['$', '$', 's']]
        self.rules = map(self.buildRule,self.patterns)

    def __call__(self,class_name):
        '''Pluralize a noun using some simple rules.'''
        for rule in self.rules:
            result = rule(class_name)
            if result: return result

pluralize = Plural()

import sqlalchemy.ext.declarative
class ModelMeta(sqlalchemy.ext.declarative.DeclarativeMeta):
    def __init__(cls, name, bases, ns):
        try:
            if Model not in bases:
                return
        except NameError:
            return
        # set the tablename, if it's user set, use that, otherwise use a function to create one
        cls.__tablename__ = getattr(cls, "__tablename__" , pluralize(name.lower())) 
        # tableargs adds autoload to create schema reflection
        cls.__table_args__ = ({'autoload':True})
        super(ModelMeta, cls).__init__(name, bases, ns)

class Model(Base):
    '''Pybald Model class, inherits from SQLAlchemy Declarative Base.'''
    __metaclass__ = ModelMeta
    
    NotFound = sqlalchemy.orm.exc.NoResultFound
    
    def save(self,commit=True):
        '''Save this instance. When commit is False, stages data for later commit.'''
        db.add(self)
        
        if commit:
            self.commit()
        return self

    def commit(self):
        '''Call the commit for the entire session (includes anything else pending)'''
        db.commit()

    @classmethod
    def get(cls,**where):
        '''Builds a sqlalchemy load query to return stored objects and executes it.'''
        return cls.load(**where).one()

    @classmethod
    def load(cls,**where):
        '''Builds a sqlalchemy load query to return stored objects. Must execute the query to retrieve.'''
        return db.query(cls).filter_by(**where)

    @classmethod
    def query(cls):
        return db.query(cls)

    @classmethod
    def load_list(cls,arg):
        return db.query(cls).filter(arg)


# model commands

def create():
    '''Create all tables.'''
    Base.metadata.create_all()


