# Generated by Django 3.2.7 on 2021-10-07 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20211007_0640'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Watchlist',
            new_name='WatchedListing',
        ),
    ]
