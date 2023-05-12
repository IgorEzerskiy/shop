from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from main_app.models import Product, Purchase, User, PurchaseReturns
from main_app.forms import ProductForm, PurchaseForm, UserCreateForm, UserForm, PurchaseReturnsCreateForm


class ProductListView(ListView):
    template_name = 'home_page.html'
    model = Product
    paginate_by = 3


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = '/'
    form_class = ProductForm
    template_name = 'product_add.html'
    success_url = '/'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    model = Product
    form_class = ProductForm
    template_name = 'product_update.html'
    success_url = '/'


class ProductDetailView(DetailView):
    template_name = 'product_item.html'
    slug_url_kwarg = 'slug'
    extra_context = {'product_quantity': PurchaseForm()}
    queryset = Product.objects.all()


class ProfileView(LoginRequiredMixin, ListView):
    login_url = 'login/'
    template_name = 'profile.html'
    queryset = Purchase.objects.all()
    paginate_by = 5
    extra_context = {'purchase_returns_form': PurchaseReturnsCreateForm()}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    model = Purchase
    success_url = '/'
    form_class = PurchaseForm
    http_method_names = ['post']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request,
                       'slug': self.kwargs['slug']})

        return kwargs

    def get_success_url(self):
        return f"/product/{self.kwargs['slug']}"

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        obj = form.save(commit=False)
        product = form.product
        obj.product = product
        obj.user = self.request.user
        product.update_quantity(amount=obj.product_quantity)
        self.request.user.update_balance(amount=product.price * obj.product_quantity)
        with transaction.atomic():
            obj.save()
            product.save()
            self.request.user.save()
        messages.success(self.request, "Purchase complete!!!")
        return super().form_valid(form=form)


class PurchaseReturnsCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    model = PurchaseReturns
    form_class = PurchaseReturnsCreateForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request.POST.get('product_id')})
        return kwargs

    def form_invalid(self, form):
        return HttpResponseRedirect('/')

    def form_valid(self, form):
        PurchaseReturns.objects.create(purchase=Purchase.objects.get(id=self.request.POST.get('product_id')))
        return super().form_valid(form=form)


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = UserForm
    next_page = '/'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    http_method_names = ['post']
    next_page = '/'


class UserCreateView(CreateView):
    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = '/'
