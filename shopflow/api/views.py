from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from shopflow.models import CartItem, Cart
from estore.models import Product
from .serializers import *
from .permissions import IsCartOwner
from rest_framework.serializers import ValidationError
class AddItemToCart(generics.CreateAPIView):
    serializer_class=CartItemPostSerializer
    queryset=CartItem.objects.all()

    def perform_create(self,serializer):
        cart=Cart.objects.get(user=self.request.user)
        product=serializer.validated_data['product']
        cart_item=CartItem.objects.filter(cart=cart,product=product)
        if cart_item.exists():
            raise ValidationError('This product is already in your cart') 
        else:
            serializer.save(cart=cart)


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


class CartItemDetail(generics.RetrieveUpdateAPIView):
    serializer_class = CartItemPostSerializer
    queryset=CartItem.objects.all()
    permission_classes=[permissions.IsAuthenticated,IsCartOwner]

    # def get_queryset(self):
    #     user=self.request.user
    #     cart = Cart.objects.get(user=user)
    #     cart_items = CartItem.objects.filter(cart=cart)
    #     return cart_items
