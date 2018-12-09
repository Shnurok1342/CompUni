from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from .views_ld import CategoryListMixin
from .models import Category, Product, ProductImage
from .forms import ProductForm, ProductImageInlineFormSet

class ProductCreate(CategoryListMixin, TemplateView):
    form = None
    productimage_forms = None
    template_name = "products/product_form/product_add.html"

    def get(self, request, *args, **kwargs):
        if self.kwargs["category_id"] == None:
            category = Category.objects.first()
        else:
            category = Category.objects.get(id = self.kwargs["category_id"])
        self.form = ProductForm(initial = {"category": category.id, "is_active": True})
        self.productimage_forms = ProductImageInlineFormSet(
            queryset = ProductImage.objects.none()
        )
        return super(ProductCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductCreate, self).get_context_data(**kwargs)
        context["category"] = Category.objects.get(id = self.kwargs["category_id"])
        context["form"] = self.form
        context["formset"] = self.productimage_forms
        return context

    def post(self, request, *args, **kwargs):
        self.form = ProductForm(request.POST)
        self.productimage_forms = ProductImageInlineFormSet(
            request.POST,
            request.FILES,
            queryset = ProductImage.objects.none()
        )
        if self.form.is_valid() and self.productimage_forms.is_valid():
            product = self.form.save()
            product_images = self.productimage_forms.save(commit = False)
            for product_image in product_images:
                product_image.product = product
                product_image.save()
            return redirect("products_info", category_id = product.category.id)
        else:
            return super(ProductCreate, self).get(request, *args, **kwargs)

class ProductUpdate(CategoryListMixin, TemplateView):
    form = None
    productimage_forms = None
    category = None
    template_name = "products/product_form/product_edit.html"

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id = self.kwargs["product_id"])
        self.form = ProductForm(instance = product)
        self.productimage_forms = ProductImageInlineFormSet(
            instance = product
        )
        if self.kwargs["category_id"] == None:
            self.category = None
        else:
            self.category = Category.objects.get(id = self.kwargs["category_id"])
        return super(ProductUpdate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductUpdate, self).get_context_data(**kwargs)
        context["product"] = Product.objects.get(id = self.kwargs["product_id"])
        context["form"] = self.form
        context["formset"] = self.productimage_forms
        if self.category:
            context["category"] = self.category
        return context

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id = self.kwargs["product_id"])
        self.form = ProductForm(request.POST, instance = product)
        self.productimage_forms = ProductImageInlineFormSet(
            request.POST,
            request.FILES,
            instance = product
        )
        if self.form.is_valid() and self.productimage_forms.is_valid():
            self.form.save()
            product_images = self.productimage_forms.save(commit = False)
            for del_product_image in self.productimage_forms.deleted_objects:
                del_product_image.delete()
            for product_image in product_images:
                product_image.product = product
                product_image.save()
            return redirect("products_info", category_id = product.category.id)
        else:
            return super(ProductUpdate, self).get(request, *args, **kwargs)

class ProductDelete(CategoryListMixin, TemplateView):
    form = None
    category = None
    template_name = "products/product_form/product_delete.html"

    def get(self, request, *args, **kwargs):
        self.form = ProductForm()
        if self.kwargs["category_id"] == None:
            self.category = None
        else:
            self.category = Category.objects.get(id = self.kwargs["category_id"])
        return super(ProductDelete, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form = ProductForm(request.POST)
        if self.kwargs["product_id"] != None:
            product = Product.objects.get(id = self.kwargs["product_id"])
            product.delete()
            return redirect("products_info", category_id = product.category.id)
        else:
            return super(ProductDelete, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDelete, self).get_context_data(**kwargs)
        context["product"] = Product.objects.get(id = self.kwargs["product_id"])
        if self.category:
            context["category"] = self.category
        return context
