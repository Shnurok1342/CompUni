from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View

from products.models import Product
from .filters import ProductFilter

class ESearchView(View):
    template_name = 'search/search_list.html'

    def get(self, request, *args, **kwargs):
        context = {}
        question = request.GET.get('q')
        if question is not None:
            search_products = Product.objects.filter(name__search=question)
            context['last_question'] = '?q=%s' % question
            current_page = Paginator(search_products, 2)
            page = request.GET.get('page')
            try:
                context['product_lists'] = current_page.page(page)
            except PageNotAnInteger:
                context['product_lists'] = current_page.page(1)
            except EmptyPage:
                context['product_lists'] = current_page.page(current_page.num_pages)
        return render(request, template_name=self.template_name, context=context)

class EFilterView(View):
    template_name = 'search/filter_list.html'

    def get(self, request, *args, **kwargs):
        context = {}
        product_list = Product.objects.all()
        product_filter = ProductFilter(request.GET, queryset=product_list)
        context['filter_form'] = product_filter.form
        if request.GET.urlencode():
            current_page = Paginator(product_filter.qs, 2)
            context['filter_code'] = '?' + request.GET.urlencode()
            page = request.GET.get('page')
            try:
                context['product_lists'] = current_page.page(page)
            except PageNotAnInteger:
                context['product_lists'] = current_page.page(1)
            except EmptyPage:
                context['product_lists'] = current_page.page(current_page.num_pages)
        return render(request, template_name=self.template_name, context=context)
