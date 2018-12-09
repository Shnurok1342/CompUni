from django import forms
from phonenumber_field import formfields

class CheckoutContactForm(forms.Form):
    client_name = forms.CharField(required = True)
    client_phone = formfields.PhoneNumberField(required = True)
