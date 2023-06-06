import datetime

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.forms.fields import ImageField
from main_app.models import Product, User, Purchase, PurchaseReturns
from rest_framework.exceptions import ValidationError

from shop import settings


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


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class PurchaseSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

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


class PurchaseReturnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReturns
        fields = ['id', 'purchase', 'purchase_return_time']

    def validate(self, data):
        purchased_at = data['purchase'].purchase_time.replace(tzinfo=datetime.timezone.utc)
        datetime_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        time_delta = datetime.timedelta(minutes=settings.ALLOWED_RETURN_TIME)
        time_edge = purchased_at + time_delta

        if datetime_now > time_edge:
            raise ValidationError('You can not create a refund, time is up!!!')

        if self.context['request'].user.id != data['purchase'].user.id:
            raise ValidationError('The user in the request is not the one who made the purchase!!!')
