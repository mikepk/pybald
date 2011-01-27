import random
import hashlib
from pybald.db import models
import copy

def gen_id():
    '''Generate a session_id key for the session'''
    # user current time as seed
    random.seed()
    # choose a random num up to 2^32
    key = random.randint(1,2**32)
    # hash it for a unique session_id
    return hashlib.sha1('SALT SALT SALT SALT'+str(key)).hexdigest()

class Session(models.Model):
    session_id = models.Column(models.String(128), nullable=False, default=gen_id)
    cache = models.Column(models.PickleType(mutable=False), default={})
    user_id = models.Column(models.ForeignKey('users.id'), default=0)
    user =  models.relationship("User")
    date_modified = models.Column(models.TIMESTAMP, server_default=models.func.current_timestamp(), onupdate=models.func.current_timestamp() )


    def __init__(self):
        self.session_dirty = False
        self.stash_data = None

    @models.reconstructor
    def __orm_init__(self):
        self.__init__()

    def stash(self,data=None):
        '''Stashes data in the session for one request.'''
        if data:
            self.cache = copy.copy(self.cache)
            self.cache['stash'] = data
            self.stash_data = data
            self.session_dirty = True
        return self.stash_data

    def _pre(self,req):
        self.stash_data = self.cache.get('stash',None)
        if self.stash_data:
            self.cache = copy.copy(self.cache)
            del self.cache['stash']
            self.session_dirty = True

    def _post(self,req,resp):
        if self.session_dirty:
            self.save(True)
        # re close the session
        models.session.remove()

    def __repr__(self):
        return unicode("<Session('%s','%s','%s', '%s')>" % (self.id, self.session_id, self.user_id, self.date_modified))


    # # Caching
    # # ==================
    # @classmethod
    # def get(cls, *pargs, **kargs):
    #     key = kargs["session_id"]
    #     cached_object = mc.get(str("session:"+key))
    #     if cached_object:
    #         cached_object = models.session.merge(cached_object, load=False)
    #     else:
    #         cached_object = super(Session, cls).load(*pargs, **kargs).options(models.eagerload("user"), models.eagerload("user.profile"), models.eagerload("user.profile.picture")).one()
    #         mc.set(str("session:"+str(key)), cached_object)
    #     return cached_object
    # 
    # def save(self, *pargs, **kargs):
    #     super(Session, self).save(*pargs, **kargs)
    #     return mc.set(str("session:"+str(self.session_id)), self)
    # 
    # def delete(self):
    #     return mc.delete(str("session:"+self.id))
