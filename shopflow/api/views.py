from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from shopflow.models import CartItem, Cart
from estore.models import Product
from .serializers import *


# class AddItemToCart(generics.CreateAPIView):
#     serializer_class = CartItemPostSerializer
    # def post(self, request):
    #     user=self.request.user
    #     cart=Cart.objects.get(user=user)
    #     product_id=self.request.data.get('product_id')
    #     print(product_id)
    #     quantity=self.request.data.get('quantity')
    #     product=Product.objects.get(id=1)
    #     cart_item,created=CartItem.objects.get_or_create(cart=cart,product=product)
    #     if not created:
    #         cart_item.quantity+=quantity
    #     else:
    #         cart_item.quantity=quantity
    #     cart_item.save()

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # def perform_create(self,serializer):
    #     user=self.request.user
    #     cart=Cart.objects.get(user=user)
    #     item=serializer.save(cart=cart)
    #     cart.products.add(item)
    #     cart.save()

    
class AddItemToCart(APIView):
    def post(self, request):
        data = request.data
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id=data.get('product')
        quantity=data.get('quantity')
        try:
            product=Product.objects.get(id=product_id,is_active=True)
        except Product.DoesNotExist:
            return Response('Product not found')
        try:
            cartItem=CartItem.objects.get(cart=cart,product=product)
            if product.stock_quantity>=cartItem.quantity:
                            cartItem.quantity+=quantity
                            cartItem.save()
                            cart.products.add(cartItem.product)
                            cart.save()
                            response_data = {"message": "Quantity updated", "cart_item": CartItemGetSerializer(cartItem).data}
                            return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response ({"error": f"This quantity exceeds stock quantity. You can only choose {product.stock_quantity} product."})
        except CartItem.DoesNotExist:
                    data['cart'] = cart.id
                    serializer = CartItemPostSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListItemOfCart(APIView):
    def get(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)
            serializer = CartItemGetSerializer(cart_items, many=True)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart does not exist'}, status=status.HTTP_404_NOT_FOUND)




        # product_id = request.data.get('product')
        # quantity=request.data.get('quantity')
        # try:
        #     product = Product.objects.get(id=product_id)
        # except Product.DoesNotExist:
        #     return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        # # user = request.user
        # # cart= Cart.objects.get(user=user)

        # # cart.products.add(product)
        # # cart.save()
