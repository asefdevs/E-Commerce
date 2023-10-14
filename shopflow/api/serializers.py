from rest_framework import serializers
from shopflow.models import CartItem, Cart,Favorites
from estore.models import Product

class CartItemGetSerializer(serializers.ModelSerializer):
    cart = serializers.StringRelatedField()
    product=serializers.StringRelatedField()
    class Meta:
        model = CartItem
        fields = '__all__'

        
class CartItemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields=['quantity', 'product']

    def validate_quantity(self,value):
        product_id=self.initial_data.get('product')
        quantity=value
        product=Product.objects.get(id=product_id)
        if product.stock_quantity<quantity:
            raise serializers.ValidationError('Quantity exceeds stock quantity')
        return value
        

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class AddFavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favorites
        exclude=['user']

    
class GetFavoritesSerializer(serializers.ModelSerializer):
    product=serializers.StringRelatedField()
    user=serializers.StringRelatedField()
    class Meta:
        model=Favorites
        fields='__all__'
        

        

