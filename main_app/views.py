from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from main_app.models import Product, Purchase, User
from main_app.forms import ProductForm, PurchaseForm, UserCreateForm


class ProductListView(TemplateView):
    template_name = 'home_page.html'
    extra_context = {'products': Product.objects.all()}


class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'product_add.html'
    success_url = '/'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    form_class = ProductForm
    template_name = 'product_update.html'
    success_url = '/'
    queryset = Product.objects.all()


class ProductV(LoginRequiredMixin, TemplateView):
    """ЭТУ НУЖНО УДАЛИТЬ ВЬЮХУ"""
    login_url = 'login/'
    template_name = 'product_list.html'
    extra_context = {'products': Product.objects.all()}


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_item.html'
    slug_url_kwarg = 'slug'
    extra_context = {'product_quantity': PurchaseForm()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object(queryset=self.model.objects)
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = 'login/'
    template_name = 'profile.html'
    # extra_context = {'purchase': Purchase.objects.filter(user=self.request.user)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase'] = Purchase.objects.filter(user=self.request.user)
        return context


class PurchaseCreateView(CreateView):
    """"""
    success_url = '/'
    form_class = PurchaseForm
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        slug = self.kwargs.get(self.slug_url_kwarg)
        obj = form.save(commit=False)
        obj.user = User.objects.get(id=self.request.user.id)
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


class UserLoginView(LoginView):
    template_name = 'login.html'
    next_page = '/'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    http_method_names = ['post']
    next_page = '/'


class UserCreateView(CreateView):
    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = '/'
