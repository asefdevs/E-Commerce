from rest_framework import serializers
from shopflow.models import *
from estore.models import Product
from estore.api.serializers import ProductListSerializer


class CartItemGetSerializer(serializers.ModelSerializer):
    cart = serializers.StringRelatedField()
    product = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        fields = '__all__'


class CartItemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity', 'product']

    def validate_quantity(self, value):
        product_id = self.initial_data.get('product')
        quantity = value
        product = Product.objects.get(id=product_id)
        if product.stock_quantity < quantity:
            raise serializers.ValidationError(
               {"message" : 'Quantity exceeds stock quantity'})
        return value


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class AddFavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        exclude = ['user']


class GetFavoritesSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Favorites
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_method']


class GetOrderSerializer(serializers.ModelSerializer):
    products=CartItemGetSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


