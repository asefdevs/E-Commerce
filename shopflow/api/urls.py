from django.urls import path
from . import views

urlpatterns = [
    path('cartitems/', views.ListItemOfCart.as_view(), name='product-cart'),
    path('add_item/', views.AddItemToCart.as_view(), name='add-item'),
    path('cartitems/<int:pk>/', views.CartItemDetail.as_view(), name='item-detail')
]
