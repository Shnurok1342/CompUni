from django import forms
from .models import Product, ProductImage, Category
from django.forms.models import inlineformset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'quantity', 'price', 'discount', 'is_active']

    name = forms.CharField(label = "Название:")
    category = forms.ModelChoiceField(queryset = Category.objects.all(), label = "Категория:", empty_label = None)
    description = forms.CharField(widget = forms.Textarea, label = "Описание:")
    quantity = forms.IntegerField(min_value = 0, label = "Наличие:", help_text = "шт.")
    price = forms.IntegerField(min_value = 0, label = "Стоимость:", help_text = "руб.")
    discount = forms.IntegerField(initial = 0, min_value = 0, max_value = 99, label = "Скидка:", help_text = "%")
    is_active = forms.BooleanField(initial = True, label = "Активен:")

ProductImageInlineFormSet = forms.inlineformset_factory(
    Product,
    ProductImage,
    fields = ('image', "is_main", "is_active", ),
    extra = 1,
    min_num = 1
)
