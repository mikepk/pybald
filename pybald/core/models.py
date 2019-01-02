from six import with_metaclass
import sqlalchemy
import sqlalchemy.orm

import sqlalchemy.ext.declarative
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm.attributes import (
    instance_state
    )
from sqlalchemy.orm.util import (
    has_identity
)
from sqlalchemy.dialects import postgresql as pg

from pybald import context
from pybald.util import camel_to_underscore, pluralize

from pybald.db import ext

# the surrogate_pk template that assures that surrogate primary keys
# are all the same and ordered with the pk first in the table
surrogate_pk_template = sqlalchemy.Column(sqlalchemy.Integer, nullable=False,
                                          primary_key=True)


def _include_sqlalchemy(obj):
    for module in sqlalchemy, sqlalchemy.orm, ext:
        for key in module.__all__:
            if not hasattr(obj, key):
                setattr(obj, key, getattr(module, key))


def make_model_class(Base, session, config=None):
    '''Create a series of classes for models that are bound to a context.'''
    if config is None:
        class BlankConfig(object):
            def __getattr__(self, key):
                return None

        config = BlankConfig()

    class ModelMeta(sqlalchemy.ext.declarative.DeclarativeMeta):
        '''
        MetaClass that sets up some common behaviors for pybald models.

        Will assign tablename if not defined based on pluralization rules. Also
        applies project global table arguments. Lastly this will assign a
        numeric primary key id to the table if no primary key was defined
        in the model class.
        '''
        def __init__(cls, name, bases, ns):
            try:
                if Model not in bases:
                    # Allow for inheritance of the Model object
                    # for use with SqlAlchemy inheritance patterns
                    super(ModelMeta, cls).__init__(name, bases, ns)
                    return
            except NameError:
                # if this is the Model class, then just return
                return

            # set the tablename, if it's user set, use that, otherwise use a
            # function to create one
            cls.__tablename__ = getattr(cls, "__tablename__",
                                        pluralize(camel_to_underscore(name)))
            # tableargs adds autoload to create schema reflection
            cls.__table_args__ = getattr(cls, "__table_args__", {})
            if config.schema_reflection:
                # create or update the __table_args__ attribute
                cls.__table_args__['autoload'] = True
            if config.global_table_args:
                cls.__table_args__.update(config.global_table_args)

            auto_create_pk = getattr(cls, "__auto_create_pk__", True)

            if cls.__table_args__.get('autoload', False):
                auto_create_pk = False

            # check if we're auto creating PKs and if the class has at least
            # one primary key if not, automatically generate an integer
            # surrogate primary key.
            if auto_create_pk:
                has_primary = any([False] + [value.primary_key
                                             for value in cls.__dict__.values()
                                             if isinstance(value, sqlalchemy.Column)])
                if not has_primary:
                    # treat the id as a mixin w/copy
                    surrogate_pk = surrogate_pk_template.copy()
                    surrogate_pk._creation_order = surrogate_pk_template._creation_order
                    cls.id = surrogate_pk
            super(ModelMeta, cls).__init__(name, bases, ns)

    class RegistryMount(type):
        '''
        A registry creating metaclass that keeps track of all defined classes that
        inherit from a base class using this metaclass.
        '''
        # lifted almost verbatim from: http://martyalchin.com/2008/jan/10/simple-plugin-framework/
        def __init__(cls, name, bases, attrs):
            try:
                cls.registry.append(cls)
            except AttributeError:
                # this is processing the first class (the mount point)
                cls.registry = [] #context.model_registry

            return super(RegistryMount, cls).__init__(name, bases, attrs)

    class RegistryModelMeta(RegistryMount, ModelMeta):
        pass

    class Model(with_metaclass(RegistryModelMeta, Base)):
        '''Pybald Model class, inherits from SQLAlchemy Declarative Base.'''
        NotFound = sqlalchemy.orm.exc.NoResultFound
        MultipleFound = sqlalchemy.orm.exc.MultipleResultsFound

        def is_modified(self):
            '''Check if SQLAlchemy believes this instance is modified.'''
            return instance_state(self).modified

        def clear_modified(self):
            '''
            Unconditionally clear all modified state from the attibutes on
            this instance.
            '''
            return instance_state(self)._commit_all({})

        def is_persisted(self):
            '''
            Check if this instance has ever been persisted. Means it is either
            `detached` or `persistent`.
            '''
            return has_identity(self)

        def save(self, flush=False):
            '''
            Saves (adds) this instance in the current databse session.

            This does not immediatly persist the data since these operations
            occur within a transaction and the sqlalchemy unit-of-work pattern.
            If something causes a rollback before the session is committed,
            these changes will be lost.

            When flush is `True`, flushes the data to the database immediately
            **within the same transaction**. This does not commit the transaction,
            for that use :py:meth:`~pybald.db.models.Model.commit`)
            '''

            session.add(self)

            if flush:
                self.flush()
            return self

        def delete(self, flush=False):
            '''
            Delete this instance from the current database session.

            The object will be deleted from the database at the next commit. If
            you want to immediately delete the object, you should follow this
            operation with a commit to emit the SQL to delete the item from
            the database and commit the transaction.
            '''
            session.delete(self)
            if flush:
                self.flush()
            return self

        def flush(self):
            '''
            Syncs all pending SQL changes (including other pending objects) to
            the underlying data store within the current transaction.

            Flush emits all the relevant SQL to the underlying store, but does
            **not** commit the current transaction or close the current
            database session.
            '''
            session.flush()
            return self

        def commit(self):
            '''
            Commits the entire database session (including other pending objects).

            This emits all relevant SQL to the databse, commits the current
            transaction, and closes the current session (and database connection)
            and returns it to the connection pool. Any data operations after this
            will pull a new database session from the connection pool.
            '''
            session.commit()
            return self

        @classmethod
        def get(cls, **where):
            '''
            A convenience method that constructs a load query with keyword
            arguments as the filter arguments and return a single instance.
            '''
            return cls.load(**where).one()

        @classmethod
        def all(cls, **where):
            '''
            Returns a collection of objects that can be filtered for
            specific collections.

            all() without arguments returns all the items of the model type.
            '''
            return cls.load(**where).all()

        # methods that return queries (must execute to retrieve)
        # =============================================================
        @classmethod
        def load(cls, **where):
            '''
            Convenience method to build a sqlalchemy query to return stored
            objects.

            Returns a query object. This query object must be executed to retrieve
            actual items from the database.
            '''
            if where:
                return session.query(cls).filter_by(**where)
            else:
                return session.query(cls)

        @classmethod
        def filter(cls, *pargs, **kargs):
            '''
            Convenience method that auto-builds the query and passes the filter
            to it.

            Returns a query object.
            '''
            return session.query(cls).filter(*pargs, **kargs)

        @classmethod
        def query(cls):
            '''
            Convenience method to return a query based on the current object
            class.
            '''
            return session.query(cls)

        @classmethod
        def show_create_table(cls):
            '''
            Uses the simple dump_engine to print to stdout the SQL for this
            table.
            '''
            cls.__table__.create(context.dump_engine)

    class NonDbModel(with_metaclass(RegistryMount, object)):
        '''
        A plain Python object that uses the RegistryMount system to register
        non database models. Inheriting from this allows the object to be registered
        as a Model.
        '''
        # __metaclass__ = RegistryMount
        # use the same registry space for NonDbModels
        registry = Model.registry

    return Model, NonDbModel


class ContextBoundModels(object):
    '''Creates a 'bound' set of model definitions to a particular context'''
    def __init__(self, config=None):
        if config:
            self.config = config
        else:
            self.config = context.config
        _include_sqlalchemy(self)
        self.engine = self.create_engine(self.config.database_engine_uri,
                                         **self.config.database_engine_args)
        self.db = self.create_session(engine=self.engine)
        self.Base = declarative_base(bind=self.engine)
        self.Model, self.NonDbModel = make_model_class(self.Base, self.db, self.config)

    def create_session(self, engine=None, session_args=None):
        # build session
        if session_args is None:
            session_args = {}
        session = self.scoped_session(self.sessionmaker(bind=engine, **session_args))
        return session
