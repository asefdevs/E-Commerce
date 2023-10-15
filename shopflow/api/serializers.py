from rest_framework import serializers
from shopflow.models import CartItem, Cart,Favorites,Order
from estore.models import Product
from estore.api.serializers import ProductListSerializer
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

class CreateOrderSerializer(serializers.ModelSerializer):
    # products=serializers.SerializerMethodField()
    class Meta:
        model=Order
        fields=['payment_method']

    # def get_products(self,obj):
    #     cart=obj.cart
    #     cart_items=CartItem.objects.filter(cart=cart)
    #     products = [item.product for item in cart_items]
    #     product_serializer=ProductListSerializer(products,many=True)
    #     return product_serializer.data
    
class GetOrderSerializer(serializers.ModelSerializer):
    products=serializers.SerializerMethodField()
    
    class Meta:
        model=Order
        fields=['payment_method','products','cart']

    def get_products(self,obj):
        cart=obj.cart
        cart_items=CartItem.objects.filter(cart=cart)
        products = [item.product for item in cart_items]
        product_serializer=ProductListSerializer(products,many=True)
        return product_serializer.data



        

