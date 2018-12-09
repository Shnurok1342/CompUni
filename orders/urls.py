from django.urls import path
from . import views

urlpatterns = [
    path('basket_adding', views.basket_adding, name='basket_adding'),
    path('checkout/create', views.checkout, name='checkout_create'),
    path('checkout/success/<int:order_id>', views.checkout_success, name='checkout_success'),
]
