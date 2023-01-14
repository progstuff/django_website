# Generated by Django 4.1.4 on 2023-01-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_cite', '0013_remove_purchase_amount_remove_purchase_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='store',
        ),
        migrations.RemoveField(
            model_name='productpurchased',
            name='store',
        ),
        migrations.RemoveField(
            model_name='review',
            name='store',
        ),
        migrations.RemoveField(
            model_name='storage',
            name='store',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='delivery_state',
            field=models.CharField(choices=[('С', 'Собирается'), ('Д', 'Доставляется'), ('Г', 'Готов к выдаче'), ('В', 'Выдан покупателю')], default='С', max_length=1, verbose_name='Статус доставки'),
        ),
        migrations.DeleteModel(
            name='Basket',
        ),
        migrations.DeleteModel(
            name='Delivery',
        ),
        migrations.DeleteModel(
            name='Store',
        ),
    ]