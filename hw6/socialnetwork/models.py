# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user            = models.OneToOneField(User, primary_key=True)
    picture         = models.FileField(upload_to="images", blank=True)
    bio             = models.CharField(max_length=420, default="Write a short bio...", blank=True)
    content_type    = models.CharField(blank=True, max_length=50)
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


class Post(models.Model):

    text            = models.CharField(blank=True, max_length=400)
    created_by      = models.ForeignKey(User, related_name="entry_creators")  # a user can create many posts
    creation_time   = models.DateTimeField()
    last_changed    = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return 'Post(id=' + str(self.id) + ')'




class Comment(models.Model):

    content         = models.CharField(max_length=400)
    post            = models.ForeignKey(Post) # a post can have many comments
    created_by      = models.ForeignKey(User)  # a user can create many comments
    created_time    = models.DateTimeField()
    last_changed    = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'User(id=' + str(self.id) + ')'
