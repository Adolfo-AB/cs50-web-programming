# Generated by Django 3.2.7 on 2021-10-21 18:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='get_following', to=settings.AUTH_USER_MODEL),
        ),
    ]