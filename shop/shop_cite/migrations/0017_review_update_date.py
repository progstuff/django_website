# Generated by Django 4.1.4 on 2023-01-16 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_cite', '0016_purchase_total_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата отзыва'),
        ),
    ]
