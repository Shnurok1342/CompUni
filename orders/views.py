from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from accounts.models import UserProfile
from .models import *
from .forms import CheckoutContactForm

# Create your views here.
def basket_adding(request):
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")
    if is_delete == 'true':
        product = ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key = session_key, product_id = product_id, is_active = True, defaults={'nmb': nmb})
        if not created:
            new_product.nmb += int(nmb)
            new_product.save(force_update = True)

    is_fast = data.get("is_fast")
    if is_fast == 'true':
        return redirect("checkout_create")
    # common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key = session_key, is_active = True)
    products_total_nmb = products_in_basket.count()
    return_dict = dict()
    return_dict["products_total_nmb"] = products_total_nmb
    if products_in_basket.exists():
        return_dict["products"] = list()
        for item in products_in_basket:
            product_dict = dict()
            product_dict["id"] = item.id
            product_dict["name"] = item.product.name
            product_dict["price_per_item"] = item.price_per_item
            product_dict["nmb"] = item.nmb
            return_dict["products"].append(product_dict)
    return JsonResponse(return_dict)

def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key = session_key, is_active = True).exclude(order__isnull = False)
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            data = request.POST
            name = data.get("client_name")
            phone = data.get("client_phone")
            user_profile, created = UserProfile.objects.get_or_create(phone_number = phone, defaults = {"profile_name": name})
            order = Order.objects.create(user_profile = user_profile, status_id = 1, total_price = 0)
            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id = product_in_basket_id)
                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.is_active = False
                    product_in_basket.save(force_update = True)
                    ProductInOrder.objects.create(product = product_in_basket.product,
                                                  nmb = product_in_basket.nmb,
                                                  price_per_item = product_in_basket.price_per_item,
                                                  total_price = product_in_basket.total_price,
                                                  order = order)
                    order.total_price = order.total_price + product_in_basket.price_per_item * int(product_in_basket.nmb)
                    ProductInBasket.objects.filter(id = product_in_basket_id).delete()
            order.save(force_update = True)
            return redirect("checkout_success", order_id = order.id)
        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())

def checkout_success(request, order_id):
    order = Order.objects.get(id=order_id)
    products_in_order = ProductInOrder.objects.filter(order = order)
    session_key = request.session.session_key
    if not session_key:
        request.session["session_key"] = 123
        request.session.cycle_key()
    return render(request, 'orders/checkout_success.html', locals())

from django.views.generic.base import ContextMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Order, ProductInOrder

# класс ContextMixin - создает контекст данных (context)
# поэтому наследуем его, чтобы добавить свое в контекст (например список категорий)
class PageListMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(PageListMixin, self).get_context_data(**kwargs)
        try:
            context["pn"] = self.request.GET["page"]
        except KeyError:
            context["pn"] = 1
        return context

class OrderListView(ListView, PageListMixin):
    template_name = "orders/orders_ld.html"
    paginate_by = 2

    def get_queryset(self):
        return Order.objects.order_by('id')

# класс DetailView - класс для вывода информации определенной записи
class OrderDetailView(PageListMixin, DetailView):
    template_name = "orders/order.html"
    model = Order
    pk_url_kwarg = "order_id"
    products_in_order = None

    def get(self, request, *args, **kwargs):
        self.products_in_order = ProductInOrder.objects.filter(order__id = self.kwargs["order_id"])
        return super(OrderDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        if self.products_in_order:
            context["products_in_order"] = self.products_in_order
        return context
