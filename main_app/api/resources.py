from django.db import transaction
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter

from main_app.api.permissions import IsAdminOrReadOnly
from main_app.api.serializers import ProductSerializer, UserSerializer, PurchaseSerializers
from main_app.models import Product, User, Purchase, PurchaseReturns
from shop import settings


class ProductModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PurchaseModelViewSet(viewsets.ModelViewSet):
    """Use ?search=<user_id> for render purchase list in profile page"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializers
    filter_backends = [SearchFilter]
    search_fields = ['user__id']

    def get_serializer_context(self):
        context = super(PurchaseModelViewSet, self).get_serializer_context()
        context.update({"user": self.request.user})
        return context

    def perform_create(self, serializer):
        serializer.validated_data['product'].quantity -= serializer.validated_data['product_quantity']
        self.request.user.wallet -= serializer.validated_data['product'].price * \
                                    serializer.validated_data['product_quantity']
        with transaction.atomic():
            self.request.user.save()
            serializer.validated_data['product'].save()
            serializer.save()

