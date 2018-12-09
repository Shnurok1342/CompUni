from django.urls import path, re_path

# Классы-контроллеры для вывода записей (наследники классов ListView и DetailView)
from .views_ld import ProductListView, ProductDetailView
# Классы-контроллеры для обработки записей form (наследники класса TemplateView)
from .views_form import ProductCreate, ProductUpdate, ProductDelete
from django.contrib.auth.decorators import permission_required

urlpatterns = [
    re_path(r'^(?:(?P<category_id>\d+)/)?$', ProductListView.as_view(), name = 'products_info'),
    re_path(r'^(?:(?P<category_id>\d+)/)?product/(?P<product_id>\d+)/$', ProductDetailView.as_view(), name='product'),
    path('<int:category_id>/add', permission_required("products.add_product")(ProductCreate.as_view()), name='product_add'),
    re_path(r'^(?:(?P<category_id>\d+)/)?product/(?P<product_id>\d+)/edit/$', permission_required("products.change_product")(ProductUpdate.as_view()), name='product_edit'),
    re_path(r'^(?:(?P<category_id>\d+)/)?product/(?P<product_id>\d+)/delete/$', permission_required("products.delete_product")(ProductDelete.as_view()), name='product_delete'),
]
