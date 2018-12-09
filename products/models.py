from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 64, blank = True, null = True, default = None, unique = True)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товара'

class Product(models.Model):
    name = models.CharField(max_length = 64, blank = True, null = True, default = None)
    category = models.ForeignKey(Category, on_delete = models.SET_DEFAULT, blank = True, null = True, default = None)
    description = models.TextField(blank = True, null = True, default = None)
    quantity = models.IntegerField(blank = True, null = True, default = None)
    price = models.IntegerField(blank = True, null = True, default = None)
    discount = models.IntegerField(blank = True, null = True, default = 0)
    is_active = models.BooleanField(default = True)
    date_updated = models.DateField(auto_now = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank = True, null = True, default = None)
    image = models.ImageField(upload_to = 'product_images', blank = True)
    is_active = models.BooleanField(default = True)
    is_main = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __str__(self):
        return "%s" % self.id

    def delete(self, *args, **kwargs):
        self.image.delete(save = False)
        super(ProductImage, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
