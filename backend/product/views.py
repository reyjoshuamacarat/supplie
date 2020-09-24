from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from . import models
from .forms import ProductRegistrationForm
from .models import Product
from .choices import Category as categories, Color as colors


class ProductView(View):
    def get(self, request):
        products = Product.objects.all()  # pylint: disable=no-member
        context = {
            'products': products,
        }
        return render(request, 'product/index.html', context)


class ProductRegistrationView(View):

    def get(self, request):
        context = {
            'categories': categories.choices,
            'colors': colors.choices,
        }
        return render(request, 'registration/product/index.html', context)

    def post(self, request):
        form = ProductRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            image1 = form.cleaned_data.get('image1')
            image2 = form.cleaned_data.get('image2')
            image3 = form.cleaned_data.get('image3')

            instance = form.instance

            for img in (image1, image2, image3):
                if not img:
                    continue
                product_image = models.ProductImage(product=instance, image=img)
                product_image.save()

                instance.product_images.add(product_image)

            return redirect('/product/')

        return HttpResponse(form.errors)
