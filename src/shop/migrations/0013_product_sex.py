# Generated by Django 3.1.4 on 2020-12-22 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20201222_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sex',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], default=None, max_length=7, verbose_name='Sex'),
        ),
    ]
