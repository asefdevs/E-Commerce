from django.urls import path
from . import views

urlpatterns = [
    path('cartitem/', views.ListItemOfCart.as_view(), name='product-cart'),
    path('add_item/', views.AddItemToCart.as_view(), name='add-item'),
]
