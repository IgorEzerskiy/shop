from django.contrib import admin
from main_app.models import Customer, Product, Purchase, PurchaseReturns
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseReturns)
