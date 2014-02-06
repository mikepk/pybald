from sqlalchemy.orm.attributes import instance_state

import logging
console = logging.getLogger(__name__)


def child_relationships(obj):
    '''Get instances with child relationships to this obj.'''
    for related_obj, mapper, state, data in obj.__mapper__.cascade_iterator("save-update",
                                                                         instance_state(obj)):
        yield related_obj


# Caching / invalidation event handlers and functions.
def cached_objects(iter):
    '''Return objects from a session/iterator that are tagged as cached.'''
    for obj in iter:
        # check if the sqlalchemy object is tagged for caching
        if hasattr(obj, '__memcached__'):
            yield obj


def cached_objects_with_updates(iter):
    '''Return objects from a session/iterator that are tagged for caching and
    that need an update.'''
    for obj in iter:
        if getattr(obj, "__needs_update__", False):
            yield obj


class Cache(object):
    def __init__(self, memcached, session):
        self.session = session
        self.mc = memcached

    def memc_cache(self, func):
        '''Decorates a sqlalchemy method that returns entities to check
        the the cache first for the load arguments. Otherwise runs the
        method normally and marks the returned object as needing update'''
        def replacement(*pargs, **kargs):
            key = str("|".join(["{0}:{1}".format(k, v) for (k, v) in
                                                           sorted(kargs.items())]))
            cached_object = self.mc.get(key)
            if cached_object:
                # has the object been persisted at some point? then merge
                # with SA session
                if cached_object.is_persisted():
                    cached_object = self.session.merge(cached_object, load=False)
                cached_object.__needs_update__ = False
            else:
                # fetch the object the 'normal' way
                cached_object = func(*pargs, **kargs)
                # since we got this from the database, mark it with a
                # needs_update
                cached_object.__needs_update__ = True
            # mark cached object for cache-tracking
            cached_object.__memcached__ = True
            # reconstruct the relationship list, anything that's in the current
            # relationship map add it back to the object so we know what it came
            # out of the cache with.
            cached_object.__related__ = set([child_object for child_object in
                                            child_relationships(cached_object)])
            return cached_object
        return replacement

    def check_needs_update(self, session, *pargs, **kargs):
        '''Check for objects in the SQLAlchemy session that are tagged as cached
        and are modified and then tag them for cache update on post commit.'''
        # console.debug("CHECKING FOR CACHED OBJECTS...")
        for obj in cached_objects(session):
            # console.debug("FOUND OBJECT IN SESSION MARKED AS CACHED, OBJECT: {0}".format(type(obj)))
            if obj.__needs_update__:
                continue
            related = set([cr for cr in child_relationships(obj)])
            new_related_objects = (related - obj.__related__)
            if new_related_objects:
                # console.debug("NEW CHILD OBJECTS LOADED IN SESSION: {0}".format(new_related_objects))
                obj.__needs_update__ = True
                continue
            changed = set(self.session.dirty | self.session.deleted)
            if not new_related_objects and not changed:
                continue
            if obj in changed:
                # console.debug("OBJECT IS DIRTY MARKING FOR UPDATE, OBJECT: {0}".format(type(obj)))
                obj.__needs_update__ = True
                continue
            if (changed & related):
                # console.debug("THERE ARE DIRTY CHILDREN: {0}".format(dirty_children))
                obj.__needs_update__ = True
                continue

    def update_cached_objects(self, session):
        '''Write out (or invalidate) cache entries for modified entitites'''
        for obj in cached_objects_with_updates(session):
            # record needs update to false before inserting into the cache
            obj.__needs_update__ = False
            console.debug("UPDATING MEMCACHE")
            self.mc.set(obj.cache_key, obj)

