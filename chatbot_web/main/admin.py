from django.contrib import admin
from .models import ChatSession, ChatMessage, Post

admin.site.register(ChatSession)
admin.site.register(ChatMessage)
admin.site.register(Post)