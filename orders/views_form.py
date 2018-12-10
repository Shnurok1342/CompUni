from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from .views import PageListMixin
from .models import Order, ProductInOrder
from .forms import OrderForm, ProductInOrderInlineFormSet

class OrderUpdate(PageListMixin, TemplateView):
    form = None
    productinorder_forms = None
    template_name = "orders/order_form/order_edit.html"

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id = self.kwargs["order_id"])
        self.form = OrderForm(instance = order)
        self.productinorder_forms = ProductInOrderInlineFormSet(
            instance = order
        )
        return super(OrderUpdate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context["order"] = Order.objects.get(id = self.kwargs["order_id"])
        context["form"] = self.form
        context["formset"] = self.productinorder_forms
        return context

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(id = self.kwargs["order_id"])
        self.form =OrderForm(request.POST, instance = order)
        self.productinorder_forms = ProductInOrderInlineFormSet(
            request.POST,
            instance = order
        )
        if self.form.is_valid() and self.productinorder_forms.is_valid():
            products_in_order = self.productinorder_forms.save(commit = False)
            for del_product_in_order in self.productinorder_forms.deleted_objects:
                del_product_in_order.delete()
            for product_in_order in products_in_order:
                product_in_order.order = order
                product_in_order.save()
            self.form.save()
            return redirect("orders_info")
        else:
            return super(OrderUpdate, self).get(request, *args, **kwargs)

class OrderDelete(PageListMixin, TemplateView):
    form = None
    template_name = "orders/order_form/order_delete.html"

    def get(self, request, *args, **kwargs):
        self.form = OrderForm()
        return super(OrderDelete, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form = OrderForm(request.POST)
        if self.kwargs["order_id"] != None:
            order = Order.objects.get(id = self.kwargs["order_id"])
            order.delete()
            return redirect("orders_info")
        else:
            return super(OrderDelete, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderDelete, self).get_context_data(**kwargs)
        context["order"] = Order.objects.get(id = self.kwargs["order_id"])
        context["products_in_order"] = ProductInOrder.objects.filter(order__id = self.kwargs["order_id"])
        return context
