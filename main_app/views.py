from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from main_app.models import Product, Purchase, Customer
from main_app.forms import AddProduct, Amount


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
    extra_context = {'product_quantity': Amount()}

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


class MakePurchase(CreateView):
    """"""
    success_url = '/'
    form_class = Amount
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        slug = self.kwargs.get(self.slug_url_kwarg)
        obj = form.save(commit=False)
        obj.user = Customer.objects.get(id=self.request.user.id)
        obj.product = Product.objects.get(slug=slug)
        self.success_url = f'/product/{slug}'

        if (int(self.request.POST.get('product_quantity'))) <= obj.product.quantity\
                and ((obj.product.price*int(self.request.POST.get('product_quantity'))) <= obj.user.wallet):
            with transaction.atomic():
                obj.product.update_quantity(amount=int(self.request.POST.get('product_quantity')))
                obj.user.update_balance(amount=obj.product.price*int(self.request.POST.get('product_quantity')))
            obj.save()
            return super().form_valid(form=form)
        else:
            return HttpResponseRedirect(self.success_url)


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'

    def get_success_url(self):
        return self.success_url


class Logout(LoginRequiredMixin, LogoutView):
    login_url = 'login/'
    next_page = '/'
