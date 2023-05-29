from rest_framework import serializers
from django.forms.fields import ImageField
from main_app.models import Product, User, Purchase
from rest_framework.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):
    image = ImageField(label='Image', max_length=100, required=False)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'slug', 'title', 'description',
                  'image', 'price', 'quantity']

    def validate_title(self, value):
        if not value:
            raise ValidationError('TITLE is required field!!!')
        return value

    def validate_price(self, value):
        if value <= 0:
            raise ValidationError('Price must be more then 1!!!')
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError('Quantity must be more then 0!!!')
        return value


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'wallet', 'image', 'password']

    def validate_wallet(self, value):
        if value < 0:
            raise ValidationError('Amount of money must be more then 0!!!')
        return value


class PurchaseSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Purchase
        fields = ['id', 'user', 'product', 'product_quantity', 'purchase_time']

    def validate(self, data):
        if data['product_quantity'] > data['product'].quantity:
            raise ValidationError('The quantity you entered is more than what is in stock.')

        if self.context['user'].wallet < data['product_quantity'] * data['product'].price:
            raise ValidationError('The amount of money in your wallet is less than the cost of your purchase.')
        return data

    def create(self, validated_data):
        user = self.context['user']
        validated_data['user'] = user
        purchase = Purchase.objects.create(**validated_data)
        return purchase

    def get_user(self):
        return self.context['request']
