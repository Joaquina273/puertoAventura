from django.contrib import admin
from .models import User, Post, Offer
# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Offer)
