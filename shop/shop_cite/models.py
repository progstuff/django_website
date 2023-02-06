from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime

PAYMENT_TYPE = (
    ('К', 'Онлайн картой'),
    ('Н', 'Онлайн со случайного счёта')
)
DELIVERY_TYPE = (
    ('О', 'Обычная'),
    ('Э', 'Экспресс'),
)
DELIVERY_STATE = (
    ('С', 'Собирается'),
    ('Д', 'Доставляется'),
    ('Г', 'Готов к выдаче'),
    ('В', 'Завершён'),
)
PAYMENT_STATE = (
    ('Н', 'Ожидается оплата'),
    ('О', 'Оплачен'),
)


class UserProfile(models.Model):

    USER_STATUS = (
        ('А', 'Администратор'),
        ('П', 'Покупатель'),
        ('Н', 'Незарегистрированный пользователь'),
    )

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True,
                                related_name="userprofile_user", verbose_name=_('Пользователь'))
    full_name = models.CharField(default='', max_length=1000, verbose_name=_('ФИО'))
    phone = models.CharField(default='+70000000000', max_length=12, verbose_name=_('Телефон'))
    address = models.CharField(default='', max_length=1000, verbose_name=_('Адрес'))
    town = models.CharField(default='', max_length=1000, verbose_name=_('Город'))
    status = models.CharField(default='П', max_length=1, choices=USER_STATUS, verbose_name=_('Статус'))
    payment_method = models.CharField(default='Н', max_length=1, choices=PAYMENT_TYPE, verbose_name=_('Тип оплаты'))
    delivery_type = models.CharField(default='О', max_length=1, choices=DELIVERY_TYPE, verbose_name=_('Тип доставки'))
    avatar = models.ImageField(null=True, blank=True, upload_to="images/profiles/", verbose_name=_('Иконка'))

    class Meta:
        verbose_name_plural = _('Профили пользователей')
        verbose_name = _('Профиль пользователя')

    def __str__(self):
        return self.full_name + ' ' + self.phone


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


class Review(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True,
                                     related_name="review_user", verbose_name=_('Пользователь'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                                related_name="review_product", verbose_name=_('Товар'))
    rating = models.IntegerField(default=0, verbose_name=_('Оценка'))
    description = models.CharField(max_length=1000, verbose_name=_('Текст отзыва'))
    update_date = models.DateTimeField(auto_now=True, verbose_name=_('Дата отзыва'))

    class Meta:
        verbose_name_plural = _('Отзывы')
        verbose_name = _('Отзыв')

    def __str__(self):
        return self.user_profile.full_name + ': ' + self.description


class Storage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                                related_name="storage_product", verbose_name=_('Товар'))
    amount = models.IntegerField(default=0, verbose_name=_('Количество'))

    class Meta:
        verbose_name_plural = _('Склады')
        verbose_name = _('Склад')

    def __str__(self):
        return self.product.name + ': ' + self.store.name


class Purchase(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True,
                                     related_name="purchase_user", verbose_name=_('Пользователь'))

    payment_method = models.CharField(default='Н', max_length=1, choices=PAYMENT_TYPE, verbose_name=_('Тип оплаты'))
    delivery_type = models.CharField(default='О', max_length=1, choices=DELIVERY_TYPE, verbose_name=_('Тип доставки'))
    delivery_state = models.CharField(default='С', max_length=1, choices=DELIVERY_STATE, verbose_name=_('Статус доставки'))
    payment_state = models.CharField(default='Н', max_length=1, choices=PAYMENT_STATE, verbose_name=_('Статус оплаты'))
    total_sum = models.FloatField(default=0, verbose_name=_('Сумма заказа'))
    purchase_date = models.DateTimeField(default=datetime.now, verbose_name=_('Дата покупки'))

    class Meta:
        verbose_name_plural = _('Заказы')
        verbose_name = _('Заказ')

    def __str__(self):
        return str(self.id)


class ProductPurchased(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True,
                                 related_name="product_purchase", verbose_name=_('Заказ'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                                related_name="purchase_product", verbose_name=_('Товар'))
    price = models.FloatField(default=0.0, verbose_name=_('Цена'))
    amount = models.IntegerField(default=0, verbose_name=_('Количество'))

    class Meta:
        verbose_name_plural = _('Заказанные товары')
        verbose_name = _('Заказанный товар')

    def __str__(self):
        return self.product.name
