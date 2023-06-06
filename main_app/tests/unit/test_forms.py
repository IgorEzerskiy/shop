from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest

from main_app.forms import ProductForm, PurchaseCreateForm, UserCreateForm, UserLoginForm, \
                           PurchaseReturnsCreateForm
from main_app.models import Product, User, Purchase

from django.test import TestCase, RequestFactory


class FakeMessages:
    messages = []

    def add(self, level, message, extra_tags):
        self.messages.append(str(message))

    @property
    def pop(self):
        return self.messages.pop()


class PurchaseCreateFromValidationTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.test_product = Product.objects.create(title='test', description='test description',
                                                   image=self.get_image(),
                                                   price=10, quantity=100)
        self.test_product1 = Product.objects.create(title='test_product_create', description='test description',
                                                    image=self.get_image(),
                                                    price=10, quantity=100)
        self.test_user = User.objects.create_user(username='test', password='1111')

    @staticmethod
    def get_image():
        return SimpleUploadedFile(name='fb.png', content=open('main_app/static/images/fb.png', 'rb').read(),
                                  content_type='image/jpeg')

    def test_purchase_create_form_is_valid(self):
        request = self.factory.post(path=f'create-purchase/{self.test_product.slug}')
        request.user = self.test_user

        form = PurchaseCreateForm(data={
            'product_quantity': 10
        },
            request=request,
            slug=self.test_product.slug)

        self.assertTrue(form.is_valid())

    def test_purchase_create_form_is_invalid_when_wallet_zero(self):
        request = self.factory.post(path=f'create-purchase/{self.test_product.slug}')
        request._messages = FakeMessages()
        request.user = self.test_user
        request.user.wallet = 0

        form = PurchaseCreateForm(data={
            'product_quantity': 10
        },
            request=request,
            slug=self.test_product.slug)

        self.assertFalse(form.is_valid())

    def test_purchase_create_form_is_invalid_when_request_quantity_more_than_product_quantity(self):
        request = self.factory.post(path=f'create-purchase/{self.test_product.slug}')
        request._messages = FakeMessages()
        request.user = self.test_user

        form = PurchaseCreateForm(data={
            'product_quantity': 10000
        },
            request=request,
            slug=self.test_product.slug)

        self.assertFalse(form.is_valid())


class ProductFormUpdateTestCases(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.test_product = Product.objects.create(title='test_product', description='test description',
                                                   image=self.get_image('main_app/static/images/fb.png'),
                                                   price=10, quantity=100)
        self.test_user = User.objects.create_user(username='test', password='1111')

    @staticmethod
    def get_image(path):
        return SimpleUploadedFile(name='fb.png', content=open(path, 'rb').read(),
                                  content_type='image/jpeg')

    def test_product_form_is_valid(self):
        request = self.factory.post(path=f'edit-product/{self.test_product.slug}')
        request._messages = FakeMessages()
        request.user = self.test_user

        form = ProductForm(data={
            'title': 'test case',
            'description': 'test description case',
            'price': 10,
            'quantity': 10,
            'image': self.get_image('main_app/static/images/111.png')
        })
        self.assertTrue(form.is_valid())
