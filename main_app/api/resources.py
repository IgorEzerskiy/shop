from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from main_app.api.permissions import IsAdminOrReadOnly, IsAdminOrPermissionDenied
from main_app.api.serializers import ProductSerializer, UserSerializer, PurchaseSerializers, PurchaseReturnsSerializer
from main_app.models import Product, User, Purchase, PurchaseReturns


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


class PurchaseReturnsCreateApiView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    http_method_names = ['get']


class PurchaseReturnsDeleteApiView(DestroyAPIView):
    permission_classes = [IsAdminOrPermissionDenied]
    queryset = PurchaseReturns.objects.all()
    serializer_class = PurchaseReturnsSerializer
    http_method_names = ['delete']


class PurchaseReturnsApproveDeleteApiView(DestroyAPIView):
    permission_classes = [IsAdminOrPermissionDenied]
    queryset = PurchaseReturns.objects.all()
    serializer_class = PurchaseReturnsSerializer
    http_method_names = ['delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.purchase.user.wallet += instance.purchase.product.price * instance.purchase.product_quantity
        instance.purchase.product.quantity += instance.purchase.product_quantity

        with transaction.atomic():
            instance.purchase.user.save()
            instance.purchase.product.save()
            instance.purchase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
