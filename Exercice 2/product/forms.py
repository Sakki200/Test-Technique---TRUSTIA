from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "expiry_date"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "field-input", "maxlength": "256", "required": "true"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "field-input", "step": "0.01", "required": "true"}
            ),
            "expiry_date": forms.DateInput(
                attrs={"class": "field-input", "type": "date", "required": "true"}
            ),
        }
