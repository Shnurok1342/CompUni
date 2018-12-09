from django.views.generic.base import ContextMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import Http404
from .models import Category, Product, ProductImage

# класс ContextMixin - создает контекст данных (context)
# поэтому наследуем его, чтобы добавить свое в контекст (например список категорий)
class CategoryListMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(CategoryListMixin, self).get_context_data(**kwargs)
        try:
            context["pn"] = self.request.GET["page"]
        except KeyError:
            context["pn"] = 1
        return context

# класс ListView - класс для вывода списка записей
# по сравнению с TemplateView может еще:
# * хранить список записей в переменной (default: object_list)
# * имеет встроенную поддержку пагинации (в контексте появляются два объекта: paginator и page_obj)
class ProductListView(ListView, CategoryListMixin):
    template_name = "products/index_ld.html"
    paginate_by = 2
    category = None

    def get(self, request, *args, **kwargs):
        if self.kwargs["category_id"] == None:
            self.category = None
        else:
            self.category = Category.objects.get(id = self.kwargs["category_id"])
        return super(ProductListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        if self.category:
            context["category"] = self.category
        return context

    def get_queryset(self):
        if self.category:
            return Product.objects.filter(category = self.category).order_by("name")
        else:
            return Product.objects.order_by('name')

# класс DetailView - класс для вывода информации определенной записи
class ProductDetailView(CategoryListMixin, DetailView):
    template_name = "products/product.html"
    model = Product
    pk_url_kwarg = "product_id"
    category = None

    def get(self, request, *args, **kwargs):
        if self.kwargs["category_id"] == None:
            self.category = None
        else:
            self.category = Category.objects.get(id = self.kwargs["category_id"])
        return super(ProductDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        if self.category:
            context["category"] = self.category
        return context
