from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from main_app.models import Product, Purchase, User, PurchaseReturns
from main_app.forms import ProductForm, PurchaseCreateForm, UserCreateForm, UserLoginForm, PurchaseReturnsCreateForm


class AdminPassedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ProductListView(ListView):
    # Api done
    template_name = 'home_page.html'
    model = Product
    paginate_by = 15


class ProductCreateView(AdminPassedMixin, LoginRequiredMixin, CreateView):
    # Api done
    login_url = '/'
    form_class = ProductForm
    template_name = 'product_add.html'
    success_url = '/'


class ProductUpdateView(AdminPassedMixin, LoginRequiredMixin, UpdateView):
    # Api done
    login_url = 'login/'
    model = Product
    form_class = ProductForm
    template_name = 'product_update.html'
    success_url = '/'


class ProductDetailView(DetailView):
    # Api done
    template_name = 'product_item.html'
    extra_context = {'product_quantity': PurchaseCreateForm()}
    queryset = Product.objects.all()


class ProfileView(LoginRequiredMixin, ListView):
    # Api done
    login_url = 'login/'
    template_name = 'profile.html'
    queryset = Purchase.objects.all()
    paginate_by = 5
    extra_context = {'purchase_returns_form': PurchaseReturnsCreateForm()}

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    # Api done
    login_url = 'login/'
    model = Purchase
    success_url = '/profile'
    form_class = PurchaseCreateForm
    http_method_names = ['post']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request,
                       'slug': self.kwargs['slug']})

        return kwargs

    def form_invalid(self, form):
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        obj = form.save(commit=False)
        product = form.product
        obj.product = product
        obj.user = self.request.user
        product.quantity -= obj.product_quantity
        self.request.user.wallet -= product.price * obj.product_quantity
        with transaction.atomic():
            obj.save()
            product.save()
            self.request.user.save()
        messages.success(self.request, "Purchase complete!!!")
        return super().form_valid(form=form)


class PurchaseReturnsCreateView(LoginRequiredMixin, CreateView):
    # API done
    login_url = 'login/'
    model = PurchaseReturns
    form_class = PurchaseReturnsCreateForm
    success_url = '/profile'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_invalid(self, form):
        return HttpResponseRedirect(self.success_url)


class PurchaseReturnsListView(AdminPassedMixin, ListView):
    # API Done
    template_name = 'product_returns_list.html'
    model = PurchaseReturns
    paginate_by = 3


class PurchaseReturnsDeleteView(AdminPassedMixin, DeleteView):
    # Api done
    model = PurchaseReturns
    success_url = '/'


class PurchaseReturnsApproveDeleteView(AdminPassedMixin, DeleteView):
    # API done
    model = Purchase
    success_url = '/'

    def form_valid(self, form):
        if self.object:
            self.object.product.quantity += self.object.product_quantity
            self.object.user.wallet += self.object.product_quantity * self.object.product.price

            with transaction.atomic():
                self.object.product.save()
                self.object.user.save()
        return super().form_valid(form=form)


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = UserLoginForm
    next_page = '/'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    http_method_names = ['post']
    next_page = '/'


class UserCreateView(CreateView):
    # Api done
    template_name = 'registration.html'
    form_class = UserCreateForm
    success_url = '/'
