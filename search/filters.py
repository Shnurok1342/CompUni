from products.models import Product
import django_filters

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Название')

    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt', label='Цены от')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt', label='Цены до')

    class Meta:
        model = Product
        fields = ['name', 'category', 'price__gt', 'price__lt']

    def __init__(self, *args, **kwargs):
        super(ProductFilter, self).__init__(*args, **kwargs)
        self.filters['category'].label="Категория"
