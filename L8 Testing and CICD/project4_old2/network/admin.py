from django.contrib import admin
from .models import User, UserProfile, Post

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username" )

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "followers")

class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "datetime", "content", "likes")

		
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Post)
