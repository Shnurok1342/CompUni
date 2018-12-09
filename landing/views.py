from django.shortcuts import render
from products.models import ProductImage, Category

# Create your views here.
def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    products_images_video = products_images.filter(product__category__id=2)
    products_images_proc = products_images.filter(product__category__id=1)
    cats = Category.objects.order_by("name")
    return render(request, 'landing/home.html', locals())
