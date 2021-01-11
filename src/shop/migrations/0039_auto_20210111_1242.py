# Generated by Django 3.1.4 on 2021-01-11 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0038_auto_20201231_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='positionproduct',
            old_name='product_items',
            new_name='products_quantity',
        ),
        migrations.AlterField(
            model_name='productquantity',
            name='product',
            field=models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='products_quantity', to='shop.product'),
        ),
    ]
