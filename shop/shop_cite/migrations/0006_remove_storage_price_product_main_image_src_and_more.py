# Generated by Django 4.1.4 on 2023-01-05 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_cite', '0005_category_big_image_src_alter_category_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='main_image_src',
            field=models.CharField(default='', max_length=1000, verbose_name='Превью'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='Цена'),
        ),
        migrations.CreateModel(
            name='AdditionalProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_src', models.CharField(default='', max_length=1000, verbose_name='Изображение')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_image', to='shop_cite.product', verbose_name='Товар')),
            ],
        ),
    ]
