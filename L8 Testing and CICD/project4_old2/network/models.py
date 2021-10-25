from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, blank=True, related_name="get_following")

    def serialize(self, user):
        return {
            "id": self.user.id,
            "username": self.user.username,
            "follow_status": not user.is_anonymous and self in user.get_following.all(),
            "can_follow": self.user != user and not user.is_anonymous,
            "following": self.user.get_following.count(),
            "followers": self.followers.count(),  
        }

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="get_posts")
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=280)
    likes = models.ManyToManyField(UserProfile, blank=True, related_name="get_likes")

    def serialize(self, user):
        return {
            "id": self.id,
            "content": self.content,
            "datetime": self.datetime,
            "author_id": self.author.id,
            "author_username": self.author.user.username,
            "can_edit": self.author.user == user,
            "likes": self.likes.count(),
            "liked": not user.is_anonymous and self in UserProfile.objects.filter(user=user).first().get_likes.all()
        }