from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_products, name="products_list"),
    path("add/", views.add_product, name="add_product"),
    path("update/<uuid:product_id>/", views.update_product, name="update_product"),
    path("delete/<uuid:product_id>/", views.delete_product, name="delete_product"),
    path("invoice/", views.create_invoice, name="create_invoice"),
    path("invoice/pdf/", views.generate_invoice_pdf, name="generate_invoice_pdf"),
]
