# Generated by Django 3.1.4 on 2020-12-23 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customer'),
        ('shop', '0022_auto_20201223_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket', to='users.customer'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='promocode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket', to='shop.promocode'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feedback', to='shop.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='shop.subcategory'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='shop.category'),
        ),
        migrations.AlterField(
            model_name='value',
            name='attribute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='value_model', to='shop.attribute'),
        ),
        migrations.AlterField(
            model_name='value',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='value_model', to='shop.product'),
        ),
    ]
