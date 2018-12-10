from django.db import models
from products.models import Product
from accounts.models import UserProfile
from django.contrib.auth.models import User
from decimal import *
# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length = 24, blank = True, null = True, default = None)
    is_active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __str__(self):
        return "Статус %s" %self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'

class Order(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank = True, null = True, default = None)
    comments = models.TextField(blank = True, null = True, default = None)
    total_price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0) #total price for all products in order
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank = True, null = True, default = None)
    created = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __str__(self):
        return "Заказ %s %s" %(self.id, self.status.name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        products_in_order = ProductInOrder.objects.filter(order__id = self.id)
        self.total_price = 0
        for product_in_order in products_in_order:
            self.total_price = self.total_price + product_in_order.total_price
        super(Order, self).save(*args, **kwargs)

class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank = True, null = True, default = None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank = True, null = True, default = None)
    nmb = models.IntegerField(default = 1)
    price_per_item = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    total_price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0) #price_per_item*nmb
    is_active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __str__(self):
        return "%s" %self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        self.price_per_item = self.product.price
        self.total_price = Decimal(self.nmb) * self.price_per_item
        super(ProductInOrder, self).save(*args, **kwargs)

class ProductInBasket(models.Model):
    session_key = models.CharField(max_length = 128, blank = True, null = True, default = None)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank = True, null = True, default = None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank = True, null = True, default = None)
    nmb = models.IntegerField(default = 1)
    price_per_item = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    total_price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0) #price_per_item*nmb
    is_active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __str__(self):
        return "%s" %self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        self.price_per_item = self.product.price
        self.total_price = int(self.nmb) * self.price_per_item
        super(ProductInBasket, self).save(*args, **kwargs)
