import stripe
from django.conf import settings
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework import permissions,status
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


stripe.api_key = settings.STRIPE_SECRET_KEY


class AddOrderAPIView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create_stripe_session(self, cart):
        line_items = []
        for cart_item in cart.cart_items.all():
            product = cart_item.product
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(product.price * 100),
                    'product_data': {
                        'name': product.name,
                        'images': [f"{settings.SITE_URL}/{product.image}"]
                    }
                },
                'quantity': cart_item.quantity,
            })
        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=settings.SITE_URL + '?success=true',
            cancel_url=settings.SITE_URL + '?canceled=true',
        )
        return session.url

    def perform_create(self, serializer):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        cartitems = CartItem.objects.filter(cart=cart, is_ordered=False)
        if cartitems.exists():
            # try:
                # session_url = self.create_stripe_session(cart)
                for item in cartitems:
                    order = serializer.save(cart=cart)
                    order.products.add(item)
                    order.save()
                    item.is_ordered = True
                    item.product.stock_quantity = item.product.stock_quantity - item.quantity
                    if item.product.stock_quantity == 0:
                        item.product.is_active = False
                    item.save()
                    item.product.save()
            #     return Response({'stripe_session_url': session_url})
            # except Exception as e:
            #     raise ValidationError(
            #         {'msg': 'Failed to create Stripe session', 'error': str(e)})

        else:
            raise ValidationError(
                {'message': 'You dont have any product in yout cart'})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        try:
            session_url = self.create_stripe_session(Cart.objects.get(user=self.request.user))
        except Exception as e:
                        raise ValidationError(
                            {'msg': 'Failed to create Stripe session', 'error': str(e)})       
        response_data={'checkout':session_url}
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

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
        if current_date <= expiration_time:
            order.delete()
            return Response({'message': 'Order successfully cancelled'})
        else:
            return Response({"message": "You cannot cancel your order as it's been more than 14 days."})




# class AddOrderAPIView(generics.CreateAPIView):
#     serializer_class = CreateOrderSerializer
#     queryset = Order.objects.all()
#     permission_classes = [permissions.IsAuthenticated]

#     def create_stripe_session(self, cart):
#         line_items = []
#         for cart_item in cart.cart_items.all():
#             product = cart_item.product
#             line_items.append({
#                 'price_data': {
#                     'currency': 'usd',
#                     'unit_amount': int(product.price * 100),
#                     'product_data': {
#                         'name': product.name,
#                         'images': [f"{settings.SITE_URL}/{product.image}"]
#                     }
#                 },
#                 'quantity': cart_item.quantity,
#             })
#         session = stripe.checkout.Session.create(
#             line_items=line_items,
#             mode='payment',
#             success_url=settings.SITE_URL + '?success=true',
#             cancel_url=settings.SITE_URL + '?canceled=true',
#         )
#         return session.url

#     def perform_create(self, serializer):
#         user = self.request.user
#         cart = Cart.objects.get(user=user)
#         cartitems = CartItem.objects.filter(cart=cart, is_ordered=False)
#         if cartitems.exists():
#             # try:
#                 # session_url = self.create_stripe_session(cart)
#                 for item in cartitems:
#                     order = serializer.save(cart=cart)
#                     order.products.add(item)
#                     order.save()
#                     item.is_ordered = True
#                     item.product.stock_quantity = item.product.stock_quantity - item.quantity
#                     if item.product.stock_quantity == 0:
#                         item.product.is_active = False
#                     item.save()
#                     item.product.save()
#             #     return Response({'stripe_session_url': session_url})
#             # except Exception as e:
#             #     raise ValidationError(
#             #         {'msg': 'Failed to create Stripe session', 'error': str(e)})

#         else:
#             raise ValidationError(
#                 {'message': 'You dont have any product in yout cart'})
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         try:
#             session_url = self.create_stripe_session(Cart.objects.get(user=self.request.user))
#         except Exception as e:
#                         raise ValidationError(
#                             {'msg': 'Failed to create Stripe session', 'error': str(e)})       
#         response_data={'checkout':session_url}
#         return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)