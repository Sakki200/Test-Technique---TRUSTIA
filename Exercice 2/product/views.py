from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm


def list_products(request):
    products = Product.objects.all()
    today = date.today()
    expiring_products = [
        p for p in products if p.expiry_date and p.expiry_date <= today
    ]
    total_value = sum(p.price for p in products if p.price)
    return render(request, "product/list.html", {"products": products, "expiring_products": expiring_products, "total_value": total_value})


def add_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("products_list")
    return render(request, "product/add_product.html", {"form": form})


def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect("products_list")
    return render(request, "product/update_product.html", {"form": form})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect("products_list")

    products = Product.objects.all()
    return render(request, "product/list.html", {"products": products})
