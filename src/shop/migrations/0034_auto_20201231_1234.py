# Generated by Django 3.1.4 on 2020-12-31 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_auto_20201229_1239'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PromoCode',
            new_name='PromoCodes',
        ),
        migrations.AlterModelOptions(
            name='promocodes',
            options={'permissions': [], 'verbose_name': 'Promo code', 'verbose_name_plural': 'Promo codes'},
        ),
        migrations.RenameField(
            model_name='basket',
            old_name='promocode',
            new_name='promocodes',
        ),
    ]
