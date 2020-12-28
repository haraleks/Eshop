# Generated by Django 3.1.4 on 2020-12-24 15:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_promocode_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='Discount'),
        ),
    ]