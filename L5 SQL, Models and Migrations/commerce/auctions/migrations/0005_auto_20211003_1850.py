# Generated by Django 3.2.7 on 2021-10-03 18:50

import auctions.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_listing_starting_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('HO', 'Home'), ('EL', 'Electronics'), ('FA', 'Fashion'), ('TO', 'Toys'), ('OT', 'Other')], default='OT', max_length=64),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=models.SET(auctions.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
