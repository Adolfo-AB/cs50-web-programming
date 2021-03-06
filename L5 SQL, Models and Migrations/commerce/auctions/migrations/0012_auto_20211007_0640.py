# Generated by Django 3.2.7 on 2021-10-07 06:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20211007_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_price',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_price',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
