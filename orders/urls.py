from django.urls import path
from . import views
from .views import OrderListView, OrderDetailView
from .views_form import OrderUpdate, OrderDelete
from django.contrib.auth.decorators import permission_required

urlpatterns = [
    path('list', OrderListView.as_view(), name = 'orders_info'),
    path('<int:order_id>', OrderDetailView.as_view(), name='order'),
    path('<int:order_id>/edit', permission_required("orders.change_order")(OrderUpdate.as_view()), name='order_edit'),
    path('<int:order_id>/delete', permission_required("orders.delete_order")(OrderDelete.as_view()), name='order_delete'),
    path('basket_adding', views.basket_adding, name='basket_adding'),
    path('checkout/create', views.checkout, name='checkout_create'),
    path('checkout/success/<int:order_id>', views.checkout_success, name='checkout_success'),
]
