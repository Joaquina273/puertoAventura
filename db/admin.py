from django.contrib import admin
from .models import User, Post, Offer, Port
# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Offer)
admin.site.register(Port)
