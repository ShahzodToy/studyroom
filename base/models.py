from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length = 200)
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL,null=True)
    name = models.CharField(max_length =200)
    description = models.TextField(null=True,blank=True)
    updated = models.DateTimeField(auto_now = True)
    participantes = models.ManyToManyField(User,related_name='participantes')
    created = models.DateTimeField(auto_now_add = True)
    topic = models.ForeignKey(Topic,on_delete = models.SET_NULL,null=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created']
    
class Message(models.Model):
    room = models.ForeignKey(Room,on_delete = models.SET_NULL,null=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    user  = models.ForeignKey(User,on_delete = models.CASCADE)
    class Meta:
        ordering = ['-created','updated']

    def __str__(self):
        return self.body[:50]



