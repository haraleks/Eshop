# Generated by Django 3.1.4 on 2020-12-31 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customer'),
        ('shop', '0034_auto_20201231_1234'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('canceled', 'Canceled')], default='created', max_length=9)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='users.customer')),
                ('promo_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promo_cart', to='shop.promocodes')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'permissions': [],
            },
        ),
        migrations.RemoveField(
            model_name='positionproduct',
            name='basket',
        ),
        migrations.DeleteModel(
            name='Basket',
        ),
        migrations.AddField(
            model_name='positionproduct',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='position_product', to='shop.cart'),
        ),
    ]