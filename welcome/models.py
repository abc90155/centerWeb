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

class chatTopics(models.Model):
    #topicID = 不需要 makemigrates 時會自動產生, 見migrations/XX_initial.py 
    topicOwner = models.ForeignKey(User, null = True, on_delete = models.SET_NULL, related_name = 'chatTopic', blank = True)
    topicTitle = models.CharField(max_length = 128)
    creataDate = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.topicTitle

class replys(models.Model):
    replyBelongsTo = models.ForeignKey(chat, null = True, on_delete= models.SET_NULL, related_name = 'replyBelong')
    replyerID = models.ForeignKey(User, null = True, on_delete= models.SET_NULL, related_name = 'replyer', blank = True)
    replyDate = models.DateTimeField(default = timezone.now)
    replyContent = models.TextField()

    def __str__(self):
        return self.replyContent
    


# Define a custom user type choices
USER_TYPE_CHOICES = [
    ('cch_user', 'CCH User'),
    ('htc_user', 'HTC User'),
    ('aicenter', 'AI Center'),
]

USER_COMPANY_CHOICES = [
    ('cch', 'CCH'),
    ('htc', 'HTC'),
    ('others', 'Others'),
]

# Define a profile model that extends the user model
class Profile(models.Model):
    # Link the profile to the user model with a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add a company field as a char field with a maximum length of 100
    company = models.CharField(max_length=10, choices=USER_COMPANY_CHOICES, null=True)
    department = models.CharField(max_length=100, null=True)    
    workid = models.CharField(max_length=10, null=True)  
    # Add a last_login field as a datetime field with auto_now_add set to True
    last_login = models.DateTimeField(auto_now_add=True)
    # Add a type field as a char field with choices set to USER_TYPE_CHOICES
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # Define a string representation of the profile model
    def __str__(self):
        return self.user.username