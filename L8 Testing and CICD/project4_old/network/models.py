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

    def serialize(self, user):
        return {
            "id": self.id,
            "content": self.content,
            "datetime": self.datetime,
            "author_id": self.author.id,
            "author_username": self.author.user.username,
            "editable": self.author.user == user,
            "likes": Like.objects.filter(post=self).all().count(),
            "liked": not user.is_anonymous and self in Like.objects.filter(user=user).first().get_liked()
        }
    
class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    post = models.ForeignKey(Post, on_delete=models.SET(get_sentinel_user))

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.SET(get_sentinel_user))
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.SET(get_sentinel_user))

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(follower=models.F('followed')),
                name='users_cannot_follow_themselves'
            ),
        ]