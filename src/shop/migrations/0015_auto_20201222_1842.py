# Generated by Django 3.1.4 on 2020-12-22 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20201222_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sex',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=7, null=True, verbose_name='Sex'),
        ),
    ]
