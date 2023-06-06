from django.urls import path, include
from rest_framework import routers

from main_app.api.resources import ProductModelViewSet, UserModelViewSet, PurchaseModelViewSet, \
                                   PurchaseReturnsCreateApiView, PurchaseReturnsListApiView, \
                                   PurchaseReturnsDeleteApiView, PurchaseReturnsApproveDeleteApiView, ChangePasswordView

router = routers.SimpleRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'user', UserModelViewSet, basename='User')
router.register(r'purchases', PurchaseModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('purchase-returns-create/', PurchaseReturnsCreateApiView.as_view()),
    path('purchase-returns-read/', PurchaseReturnsListApiView.as_view()),
    path('purchase-returns-delete/<int:pk>', PurchaseReturnsDeleteApiView.as_view()),
    path('purchase-returns-approve-delete/<int:pk>', PurchaseReturnsApproveDeleteApiView.as_view()),
    path('change_password/<int:pk>/', ChangePasswordView.as_view())
]
