# Generated by Django 3.1.4 on 2020-12-24 13:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20201223_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='discount',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='Discount'),
        ),
    ]