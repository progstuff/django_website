from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime


class UserProfile(models.Model):

    USER_STATUS = (
        ('А', 'Администратор'),
        ('П', 'Покупатель'),
        ('Н', 'Незарегистрированный пользователь'),
    )
    PAYMENT_TYPE = (
        ('Б', 'Безнал'),
        ('К', 'Карта'),
        ('Н', 'Наличные'),
        ('-', 'Не указано')
    )

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True,
                                related_name="userprofile_user", verbose_name=_('Пользователь'))
    status = models.CharField(default='П', max_length=10, choices=USER_STATUS, verbose_name=_('Статус'))
    payment_method = models.CharField(default='-', max_length=10, choices=PAYMENT_TYPE, verbose_name=_('Тип оплаты'))

    class Meta:
        verbose_name_plural = _('Профили пользователей')
        verbose_name = _('Профиль пользователя')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    parent_category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Родительская категория'))
    name = models.CharField(default='', max_length=1000, verbose_name=_('Категория'))
    image_src = models.CharField(default='', max_length=1000, verbose_name=_('Иконка'))
    big_image_src = models.CharField(default='', max_length=1000, verbose_name=_('Большая иконка'))
    short_image_name = models.CharField(default='', max_length=1000, verbose_name=_('Короткое название'))
    has_subcategories = models.BooleanField(default=False, verbose_name=_('Есть подкатегории'))

    class Meta:
        verbose_name_plural = _('Категории')
        verbose_name = _('Категория')

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=1000, verbose_name=_('Название'))
    description = models.CharField(max_length=1000, verbose_name=_('Описание'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 related_name="product_category", verbose_name=_('Категория'))
    price = models.FloatField(default=0.0, verbose_name=_('Цена'))
    main_image_src = models.CharField(default='', max_length=1000, verbose_name=_('Превью'))
    add1_image_src = models.CharField(default='', max_length=1000, verbose_name=_('Доп1'))
    add2_image_src = models.CharField(default='', max_length=1000, verbose_name=_('Доп2'))
    add3_image_src = models.CharField(default='', max_length=1000, verbose_name=_('Доп3'))

    class Meta:
        verbose_name_plural = _('Товары')
        verbose_name = _('Товар')

    def __str__(self):
        return self.name


class ProductCharacteristics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                                related_name="product_characteristic", verbose_name=_('Товар'))
    group = models.CharField(max_length=1000, verbose_name=_('Группа'))
    name = models.CharField(max_length=1000, verbose_name=_('Название'))
    value = models.CharField(max_length=1000, verbose_name=_('Значение'))

    class Meta:
        verbose_name_plural = _('Характеристики')
        verbose_name = _('Характеристика')

    def __str__(self):
        return self.group + ' ' + self.name

class Store(models.Model):
    name = models.CharField(max_length=1000, verbose_name=_('Название'))
    address = models.CharField(max_length=1000, verbose_name=_('Адрес'))

    class Meta:
        verbose_name_plural = _('Магазины')
        verbose_name = _('Магазин')

    def __str__(self):
        return self.name + ' ' + self.address


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             related_name="review_user", verbose_name=_('Пользователь'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                                related_name="review_product", verbose_name=_('Товар'))
    rating = models.IntegerField(default=0, verbose_name=_('Оценка'))
    description = models.CharField(max_length=1000, verbose_name=_('Текст отзыва'))
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True,
                              related_name="review_store", verbose_name=_('Магазин'))

    class Meta:
        verbose_name_plural = _('Отзывы')
        verbose_name = _('Отзыв')

    def __str__(self):
        return self.user.username + ': ' + self.description


class Delivery(models.Model):

    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True,
                              related_name="delivery_store", verbose_name=_('Магазин'))
    address = models.CharField(max_length=1000, verbose_name=_('Адрес'))

    class Meta:
        verbose_name_plural = _('Адреса доставки магазинов')
        verbose_name = _('Адрес доставки магазина')

    def __str__(self):
        return self.store.name + ': ' + self.address


class Storage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                                related_name="storage_product", verbose_name=_('Товар'))
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True,
                              related_name="storage_store", verbose_name=_('Магазин'))
    amount = models.IntegerField(default=0, verbose_name=_('Количество'))

    class Meta:
        verbose_name_plural = _('Склады')
        verbose_name = _('Склад')

    def __str__(self):
        return self.product.name + ': ' + self.store.name


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             related_name="purchase_user", verbose_name=_('Пользователь'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                                related_name="purchase_product", verbose_name=_('Товар'))
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True,
                              related_name="purchase_store", verbose_name=_('Магазин'))
    price = models.FloatField(default=0.0, verbose_name=_('Цена'))
    amount = models.IntegerField(default=0, verbose_name=_('Количество'))
    purchase_date = models.DateTimeField(default=datetime.now, verbose_name=_('Дата покупки'))
    purchase_number = models.BigIntegerField(default=0, verbose_name=_('Номер заказа'))

    class Meta:
        verbose_name_plural = _('Покупки')
        verbose_name = _('Покупка')

    def __str__(self):
        return self.purchase_date + ': ' + self.product.name + ': ' + self.store.name


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             related_name="basket_user", verbose_name=_('Пользователь'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                                related_name="basket_product", verbose_name=_('Товар'))
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True,
                              related_name="basket_store", verbose_name=_('Магазин'))
    price = models.FloatField(default=0.0, verbose_name=_('Цена'))
    amount = models.IntegerField(default=0, verbose_name=_('Количество'))

    class Meta:
        verbose_name_plural = _('Корзины')
        verbose_name = _('Корзина')

    def __str__(self):
        return self.product.name + ': ' + self.store.name
