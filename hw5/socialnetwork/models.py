# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):

    text          = models.CharField(blank=True, max_length=400)
    created_by    = models.ForeignKey(User, related_name="entry_creators")
    creation_time = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return 'Post(id=' + str(self.id) + ')'


class Profile(models.Model):
    user            = models.OneToOneField(User, primary_key=True)
    picture         = models.FileField(upload_to="images", blank=True)
    bio = models.CharField(max_length=420, default="Write a short bio...", blank=True)
    content_type = models.CharField(blank=True, max_length=50)
    following       = models.ManyToManyField(User, related_name="following", symmetrical=False)

    def __unicode__(self):
        return 'User(id=' + str(self.id) + ')'

    @staticmethod
    def get_profile(user):
        try:
            profile = Profile.objects.get(user=user)
        except:
            print('No such profile')
        return profile

