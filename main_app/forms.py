from django import forms
from main_app.models import Product, Purchase


class ProductForm(forms.ModelForm):
    title = forms.CharField(label='ProductV name', max_length=150, required=True)
    description = forms.CharField(label='Description', max_length=1500, required=True)
    price = forms.DecimalField(label='Price', max_digits=20, decimal_places=2, required=True)
    quantity = forms.IntegerField(label='Quantity', min_value=1, required=True)
    image = forms.ImageField(label='Image', max_length=100, required=False)

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'quantity', 'image']


class PurchaseForm(forms.ModelForm):
    product_quantity = forms.IntegerField(label='Quantity', min_value=1, required=True)

    class Meta:
        model = Purchase
        fields = ['product_quantity']
