# Generated by Django 3.1.4 on 2020-12-22 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20201222_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='value',
            name='product',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='value', to='shop.product'),
        ),
    ]
