from django.contrib import admin

from .models import chat, replys, Profile
# Register your models here.
admin.site.register(chat)
admin.site.register(replys)
admin.site.register(Profile)