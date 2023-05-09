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
from django.urls import path
from main_app.views import HomePageView, ProductListView, ProfileView, Login, Logout, ProductDetailView, \
                            ProductCreateView, ProductUpdateView, PurchaseCreateView
from shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home_page'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('edit-product/<slug:slug>', ProductUpdateView.as_view(), name='product_update'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_item'),
    path('add_product/', ProductCreateView.as_view(), name='product_add'),
    path('create-purchase/<slug:slug>', PurchaseCreateView.as_view(), name='create-purchase')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
