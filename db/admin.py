from django.contrib import admin
from .models import User, Post, Offer, Port, Comment, Notification, Conversation, Message
# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Offer)
admin.site.register(Port)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Conversation)
admin.site.register(Message)