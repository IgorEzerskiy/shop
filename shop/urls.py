"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main_app.views import ProductListView, ProfileView, UserLoginView, UserLogoutView, ProductDetailView, \
                            ProductCreateView, ProductUpdateView, PurchaseCreateView, UserCreateView, \
                            PurchaseReturnsCreateView, PurchaseReturnsListView, PurchaseReturnsDeleteView,\
                            PurchaseReturnsApproveDeleteView
from shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProductListView.as_view(), name='home_page'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-product/<slug:slug>', ProductUpdateView.as_view(), name='product_update'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='product_item'),
    path('add_product/', ProductCreateView.as_view(), name='product_add'),
    path('create-purchase/<slug:slug>', PurchaseCreateView.as_view(), name='create-purchase'),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('create-return/', PurchaseReturnsCreateView.as_view(), name='create_return'),
    path('returns/', PurchaseReturnsListView.as_view(), name='show_returns'),
    path('delete/<int:pk>', PurchaseReturnsDeleteView.as_view(), name='delete_returns'),
    path('purchase-approve/<int:pk>', PurchaseReturnsApproveDeleteView.as_view(), name='approve_returns'),
    path('', include('main_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
