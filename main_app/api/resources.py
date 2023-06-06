from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main_app.api.permissions import IsAdminOrReadOnly, IsAdminOrPermissionDenied, IsOwner
from main_app.api.serializers import ProductSerializer, UserSerializer, PurchaseSerializers, \
                                     PurchaseReturnsSerializer, ChangePasswordSerializer
from main_app.models import Product, User, Purchase, PurchaseReturns


class ProductModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)


class UserCreateApiView(CreateAPIView):
    serializer_class = UserSerializer


class PasswordUpdateApiView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)


class PurchaseModelViewSet(viewsets.ModelViewSet):
    """Use ?search=<user_id> for render purchase list in profile page"""
    permission_classes = [IsOwner]
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


class PurchaseReturnsCreateApiView(CreateAPIView):
    permission_classes = [IsOwner]
    queryset = PurchaseReturns.objects.all()
    serializer_class = PurchaseReturnsSerializer

    def get_serializer_context(self):
        context = super(PurchaseReturnsCreateApiView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class PurchaseReturnsListApiView(ListAPIView):
    permission_classes = [IsAdminOrPermissionDenied]
    queryset = PurchaseReturns.objects.all()
    serializer_class = PurchaseReturnsSerializer


class PurchaseReturnsDeleteApiView(DestroyAPIView):
    permission_classes = [IsAdminOrPermissionDenied]
    queryset = PurchaseReturns.objects.all()
    serializer_class = PurchaseReturnsSerializer


class PurchaseReturnsApproveDeleteApiView(DestroyAPIView):
    permission_classes = [IsAdminOrPermissionDenied]
    queryset = PurchaseReturns.objects.all()
    serializer_class = PurchaseReturnsSerializer

    def perform_destroy(self, instance):
        instance.purchase.user.wallet += instance.purchase.product.price * instance.purchase.product_quantity
        instance.purchase.product.quantity += instance.purchase.product_quantity

        with transaction.atomic():
            instance.purchase.user.save()
            instance.purchase.product.save()
            instance.purchase.delete()
