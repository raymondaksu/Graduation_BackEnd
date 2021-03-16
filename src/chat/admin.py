from django.contrib import admin
from .models import ChatUser, Message

admin.site.register(ChatUser)
admin.site.register(Message)