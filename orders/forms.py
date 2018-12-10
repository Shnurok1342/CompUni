from django import forms
from phonenumber_field import formfields

class CheckoutContactForm(forms.Form):
    client_name = forms.CharField(required = True)
    client_phone = formfields.PhoneNumberField(required = True)

from django import forms
from .models import Order, ProductInOrder, Status
from django.forms.models import inlineformset_factory

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user_profile', 'comments', 'status']

ProductInOrderInlineFormSet = forms.inlineformset_factory(
    Order,
    ProductInOrder,
    fields = ('product', "nmb", ),
    extra = 1,
    min_num = 1
)
