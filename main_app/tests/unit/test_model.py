import mock
from rest_framework.exceptions import ValidationError

from main_app.models import User, Product, Purchase, PurchaseReturns
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile


class ProductTestCase(TestCase):
    def setUp(self) -> None:
        Product.objects.create(title='test_product', description='test description', image=self.get_image(),
                               price=10, quantity=100)

    @staticmethod
    def get_image():
        return SimpleUploadedFile(name='fb.png', content=open('main_app/static/images/fb.png', 'rb').read(),
                                  content_type='image/jpeg')

    def test_price_more_then_zero(self):
        product = Product.objects.get(title='test_product')
        self.assertTrue(expr=product.price > 0, msg='Product price less then zero.')

    def test_price_less_then_zero(self):
        product = Product.objects.get(title='test_product')
        product.price = -10
        self.assertFalse(expr=product.price > 0, msg='Product price more then zero.')

