from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from main_app.models import Product, Purchase
from main_app.forms import AddProduct


class HomePage(TemplateView):
    template_name = 'home_page.html'
    extra_context = {'products': Product.objects.all()}


class ProductAdd(LoginRequiredMixin, CreateView):
    form_class = AddProduct
    template_name = 'product_add.html'
    success_url = '/'


class ProductUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    form_class = AddProduct
    template_name = 'product_update.html'
    success_url = '/'
    queryset = Product.objects.all()


class ProductList(LoginRequiredMixin, TemplateView):
    login_url = 'login/'
    template_name = 'product_list.html'
    extra_context = {'products': Product.objects.all()}


class ProductItem(DetailView):
    model = Product
    template_name = 'product_item.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object(queryset=self.model.objects)
        return context


class Profile(LoginRequiredMixin, TemplateView):
    login_url = 'login/'
    template_name = 'profile.html'
    # extra_context = {'purchase': Purchase.objects.filter(user=self.request.user)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase'] = Purchase.objects.filter(user=self.request.user)
        return context


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'

    def get_success_url(self):
        return self.success_url


class Logout(LoginRequiredMixin, LogoutView):
    login_url = 'login/'
    next_page = '/'
