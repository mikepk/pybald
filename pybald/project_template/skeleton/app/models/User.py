from pybald.db import models

import hashlib
import base64

import re

class User(models.Model):
    email = models.Column(models.String(40))
    _password = models.Column('password', models.String(28))
    
    @classmethod
    def _hash_password(cls,text,password):
        return base64.urlsafe_b64encode( hashlib.sha1('Pybald SALT'+str(text)+'Pybald SALT'+str( password )).digest() )

    def __repr__(self):
        return unicode("<User('%s','%s', '%s')>" % (self.id, self.email, self.password))


    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self,value):
        value = self.__class__._hash_password(self.email, value)
        self._password = value
    
    @classmethod
    def check_credentials(cls,email,password):
        return cls.get(email=email,password=cls._hash_password(email,password))
    
    password = models.synonym('_password', descriptor=password)
