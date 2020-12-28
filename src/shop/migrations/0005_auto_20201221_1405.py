# Generated by Django 3.1.4 on 2020-12-21 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20201221_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='value',
            name='product',
        ),
        migrations.AddField(
            model_name='attribute',
            name='product',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='attribute', to='shop.product'),
        ),
    ]