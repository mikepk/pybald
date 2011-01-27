from pybald.db import models

import re
from urlparse import urlparse

class UserProfile(models.Model):
    user_id = models.Column(models.ForeignKey('users.id'))
    user = models.relationship('User', backref=models.backref('profile',uselist=False))
    
    first_name = models.Column(models.Unicode())
    last_name = models.Column(models.Unicode())
    link = models.Column(models.Unicode())
    bio = models.Column(models.Unicode())

    def __init__(self, first_name='', last_name='', link='', bio=''):
        self.first_name = first_name
        self.last_name = last_name
        self.link = link
        self.bio = bio

    @property
    def formatted_link(self):
        test = urlparse(self.link)
        if test.scheme:
            return test.geturl()
        else:
            return urlparse("//"+self.link, scheme="http").geturl()
