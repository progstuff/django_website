# Generated by Django 4.1.4 on 2023-01-14 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_cite', '0014_remove_delivery_store_remove_productpurchased_store_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchase',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='user',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AddField(
            model_name='purchase',
            name='user_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_user', to='shop_cite.userprofile', verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='review',
            name='user_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review_user', to='shop_cite.userprofile', verbose_name='Пользователь'),
        ),
    ]
