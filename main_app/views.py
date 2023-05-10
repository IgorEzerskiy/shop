from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from main_app.models import Product, Purchase, User
from main_app.forms import ProductForm, PurchaseForm, UserCreateForm, UserForm


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
    model = Product
    template_name = 'product_item.html'
    slug_url_kwarg = 'slug'
    extra_context = {'product_quantity': PurchaseForm()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object(queryset=self.model.objects)
        return context


class ProfileView(LoginRequiredMixin, ListView):
    login_url = 'login/'
    template_name = 'profile.html'
    queryset = Purchase.objects.all()
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


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
    form_class = UserForm
    next_page = '/'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    http_method_names = ['post']
    next_page = '/'


class UserCreateView(CreateView):
    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = '/'
