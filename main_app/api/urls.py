from django.urls import path, include
from rest_framework import routers

from main_app.api.resources import ProductModelViewSet, UserModelViewSet, PurchaseModelViewSet

router = routers.SimpleRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'users', UserModelViewSet)
router.register(r'purchases', PurchaseModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]
