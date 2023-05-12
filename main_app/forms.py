from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from main_app.models import Product, Purchase, User, PurchaseReturns


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
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        if 'slug' in kwargs:
            self.slug = kwargs.pop('slug')
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['product_quantity'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        try:
            product = Product.objects.get(slug=self.slug)
            self.product = product
            if self.request.user.wallet < cleaned_data.get('product_quantity') * product.price:
                self.add_error(None, 'Error')
                messages.error(self.request, 'The amount of money in your wallet is less than the cost of your '
                                             'purchase.')
            if cleaned_data.get('product_quantity') > product.quantity:
                self.add_error(None, 'Error')
                messages.error(self.request, 'The quantity you entered is more than what is in stock.')
        except Product.DoesNotExist:
            self.add_error(None, 'Error')
            messages.error(self.request, 'Product does not exist.')


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


class PurchaseReturnsCreateForm(forms.ModelForm):
    purchase = forms.CharField(label='purchase_slug')

    class Meta:
        model = PurchaseReturns
        fields = ['purchase']

    def __init__(self, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(PurchaseReturnsCreateForm, self).__init__(**kwargs)
        if 'request' in kwargs:
            self.fields['purchase'].widget.attrs.update({'value': '1'})

    def clean_purchase(self):
        cleaned_data = super().clean()
        try:
            purchase = Purchase.objects.get(id=self.request)
        except Product.DoesNotExist:
            self.add_error(None, 'Error')
            messages.error(self.request, 'Product does not exist.')
