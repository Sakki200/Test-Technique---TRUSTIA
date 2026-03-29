from datetime import date
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import HttpResponse


def list_products(request):
    products = Product.objects.all()
    paginator = Paginator(products, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    today = date.today()
    expiring_products = [
        p for p in products if p.expiry_date and p.expiry_date <= today
    ]
    total_value = sum(p.price for p in products if p.price)
    return render(
        request,
        "product/list.html",
        {
            "products": page_obj,
            "page_obj": page_obj,
            "expiring_products": expiring_products,
            "total_value": total_value,
        },
    )


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
    return redirect("products_list")


def create_invoice(request):
    if request.method == "POST":
        items = []

        for key, value in request.POST.items():
            if key.startswith("quantity_"):
                product_id = key.split("_")[1]
                quantity = int(value)

                if quantity > 0:
                    items.append({"product_id": product_id, "quantity": quantity})

    products = Product.objects.all()
    return render(request, "invoice/create.html", {"products": products})


def generate_invoice_pdf(request):
    if request.method == "POST":
        from xhtml2pdf import pisa

        products_ids = request.POST.getlist("product[]")
        quantities = request.POST.getlist("quantity[]")
        today = date.today()

        products = []
        subtotal = Decimal("0.00")

        for product_id, quantity in zip(products_ids, quantities):
            if product_id and int(quantity) > 0:
                product = Product.objects.get(id=product_id)
                qty = int(quantity)

                total = product.price * qty
                subtotal += total

                products.append(
                    {
                        "name": product.name,
                        "price": product.price,
                        "quantity": qty,
                        "total": total,
                    }
                )

        tax = subtotal * Decimal("0.20")
        total = subtotal + tax

        html = render_to_string(
            "invoice/pdf.html",
            {
                "products": products,
                "subtotal": subtotal,
                "tax": tax,
                "total": total,
                "date": today,
                "htc": subtotal,
            },
        )

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="facture.pdf"'

        pisa.CreatePDF(html, dest=response)

        return response

    return redirect("products_list")
