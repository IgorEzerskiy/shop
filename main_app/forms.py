from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from main_app.models import Product, Purchase, User


class ProductForm(forms.ModelForm):
    title = forms.CharField(label='Product name', max_length=150, required=True)
    description = forms.CharField(label='Description', max_length=1500, required=True)
    price = forms.DecimalField(label='Price', max_digits=20, decimal_places=2, required=True)
    quantity = forms.IntegerField(label='Quantity', min_value=1, required=True)
    image = forms.ImageField(label='Image', max_length=100, required=False)

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'quantity', 'image']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})


class PurchaseForm(forms.ModelForm):
    product_quantity = forms.IntegerField(label='Quantity', min_value=1, required=True)

    class Meta:
        model = Purchase
        fields = ['product_quantity']

    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['product_quantity'].widget.attrs.update({'class': 'form-control'})


class UserCreateForm(UserCreationForm):
    image = forms.ImageField(label='Image', max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'wallet', 'image']

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['wallet'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class UserForm(AuthenticationForm):
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
