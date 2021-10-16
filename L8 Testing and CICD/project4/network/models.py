from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=280)
    
class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    post = models.ForeignKey(Post, on_delete=models.SET(get_sentinel_user))

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.SET(get_sentinel_user))
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.SET(get_sentinel_user))