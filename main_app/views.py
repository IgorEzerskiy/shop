from django.views.generic.base import TemplateView
from main_app.models import Product


class HomePage(TemplateView):
    template_name = 'home_page.html'
    extra_context = {'products': Product.objects.all()}
