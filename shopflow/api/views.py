from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework import permissions
from shopflow.models import *
from .serializers import *
from .permissions import IsCartOwner, IsOwner
from rest_framework.serializers import ValidationError
from .pagination import CustomPagination


class AddItemToCart(generics.CreateAPIView):
    serializer_class = CartItemPostSerializer
    queryset = CartItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        product = serializer.validated_data['product']
        cart_item = CartItem.objects.filter(
            cart=cart, product=product, is_ordered=False)
        if cart_item.exists():
            raise ValidationError(
                {'message': 'This product is already in your cart'})
        else:
            serializer.save(cart=cart)


class ListItemOfCart(generics.ListAPIView):
    serializer_class = CartItemGetSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = CartItem.objects.filter(cart__user=user, is_ordered=False)
        return queryset


class CartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemPostSerializer
    queryset = CartItem.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsCartOwner]

    def perform_update(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        product = serializer.validated_data['product']
        cart_item = CartItem.objects.filter(cart=cart, product=product)
        if cart_item.exists():
            raise ValidationError(
                {'message': 'This product is already in your cart'})


class AddFavoritesView(generics.CreateAPIView):
    queryset = Favorites.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddFavoritesSerializer

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        favorites = Favorites.objects.filter(user=user, product=product)
        if favorites.exists():
            raise ValidationError(
                {'message': 'This product is already in your Favorites'})
        else:

            serializer.save(user=user)


class ListFavoritesView(generics.ListAPIView):
    serializer_class = GetFavoritesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Favorites.objects.filter(user=user)
        return queryset


class FavoritesDetailView(generics.DestroyAPIView):
    serializer_class = AddFavoritesSerializer
    queryset = Favorites.objects.all()
    permission_classes = [IsOwner]


class AddOrderAPIView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        cartitems = CartItem.objects.filter(cart=cart, is_ordered=False)
        if cartitems.exists():
            for item in cartitems:
                order = serializer.save(cart=cart)
                order.products.add(item)
                order.save()
                item.is_ordered = True
                item.product.stock_quantity = item.product.stock_quantity - item.quantity
                item.save()
                item.product.save()
        else:
            raise ValidationError(
                {'message': 'You dont have any product in yout cart'})


class RecentOrderApiView(generics.ListAPIView):
    serializer_class = GetOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(cart__user=user, is_cancelled=False)
        return orders


class CancelOrderApiView(generics.RetrieveDestroyAPIView):
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.all()

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        created_at = order.created_at
        current_date = datetime.now().date()
        expiration_time = created_at.date()+timedelta(days=14)
        print(created_at)
        print(expiration_time)
        if current_date <= expiration_time:
            order.delete()
            return Response({'message': 'Order successfully cancelled'})
        else:
            return Response({"message": "You cannot cancel your order as it's been more than 14 days."})
