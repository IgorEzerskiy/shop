from django.contrib import admin
from main_app.models import User, Product, Purchase, PurchaseReturns
# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseReturns)
