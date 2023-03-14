from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class chat(models.Model):
    chatOwner = models.ForeignKey(User, null = True, on_delete = models.SET_NULL, related_name='chat', blank = True)
    chatTitle  = models.CharField(max_length=256)
    createdData = models.DateTimeField(default=timezone.now)
    #chatReceiver = models.ForeignKey(User)
    chatReceiver = models.CharField(max_length=16)
    chatContent = models.TextField()
    
    def __str__(self):
        return self.chatTitle

"""class chatTopics(models.Model):
    topicOwner = models.ForeignKey(User, null = True, on_delete = models.SET_NULL, related_name = 'chat', blank = True)
    topicTitle = models.CharField(max_length = 128)
    creataDate = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.topicTitle"""