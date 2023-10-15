from rest_framework import generics
from rest_framework import permissions
from shopflow.models import CartItem, Cart, Favorites,Order
from .serializers import *
from .permissions import IsCartOwner,IsOwner
from rest_framework.serializers import ValidationError
from.pagination import CustomPagination
class AddItemToCart(generics.CreateAPIView):
    serializer_class = CartItemPostSerializer
    queryset = CartItem.objects.all()
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        product = serializer.validated_data['product']
        cart_item = CartItem.objects.filter(cart=cart, product=product)
        if cart_item.exists():
            raise ValidationError('This product is already in your cart')
        else:
            serializer.save(cart=cart)


class ListItemOfCart(generics.ListAPIView):
    serializer_class=CartItemGetSerializer
    pagination_class=CustomPagination
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        user=self.request.user
        queryset=CartItem.objects.filter(cart__user=user)
        return queryset



class CartItemDetail(generics.RetrieveUpdateAPIView):
    serializer_class = CartItemPostSerializer
    queryset = CartItem.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsCartOwner]


class AddFavoritesView(generics.CreateAPIView):
    queryset = Favorites.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AddFavoritesSerializer

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        favorites = Favorites.objects.filter(user=user, product=product)
        if favorites.exists():
            raise ValidationError('This product is already in your Favorites')
        else:

            serializer.save(user=user)

        serializer.save(user=user)


class ListFavoritesView(generics.ListAPIView):
    serializer_class = GetFavoritesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class=CustomPagination


    def get_queryset(self):
        user = self.request.user
        queryset = Favorites.objects.filter(user=user)
        return queryset

class FavoritesDetailView(generics.DestroyAPIView):
    serializer_class=AddFavoritesSerializer
    queryset=Favorites.objects.all()
    permission_classes=[IsOwner]


class AddOrderAPIView(generics.CreateAPIView):
    serializer_class=CreateOrderSerializer
    queryset=Order.objects.all()
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self,serializer):
        user=self.request.user
        cart=Cart.objects.get(user=user)
        serializer.save(cart=cart)
class RecentOrderApiView(generics.ListAPIView):
    serializer_class=GetOrderSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        orders=Order.objects.filter(cart__user=user)
        return orders 