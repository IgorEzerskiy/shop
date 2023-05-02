import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class Customer(AbstractUser):
    wallet = models.DecimalField(decimal_places=2, max_digits=20)

    def save(self, **kwargs):
        self.wallet = 10000
        super().save(**kwargs)


class Product(models.Model):
    slug = models.SlugField(max_length=150, unique=True)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='main_app/', max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    quantity = models.PositiveIntegerField()

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + '-' + str(self.id)
        return super().save(**kwargs)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    product_quantity = models.PositiveIntegerField()
    purchase_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product) + '-' + str(self.user) + '-' + str(self.purchase_time)


class PurchaseReturns(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name='purchase')
    purchase_return_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.purchase.user.username) + '-' + str(self.purchase_return_time)
