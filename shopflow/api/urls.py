from django.urls import path
from . import views

urlpatterns = [
    path('cartitems/', views.ListItemOfCart.as_view(), name='product-cart'),
    path('add_item/', views.AddItemToCart.as_view(), name='add-item'),
    path('cartitems/<int:pk>/', views.CartItemDetail.as_view(), name='item-detail'),
    path('add_favorites/', views.AddFavoritesView.as_view(), name='add-favorites'),
    path('favorites/', views.ListFavoritesView.as_view(), name='list-favorites'),
    path('delete_favorite/<int:pk>/',
         views.FavoritesDetailView.as_view(), name='favorites-detail'),
    path('add_order/', views.AddOrderAPIView.as_view(), name='add_order'),
    path('recent_orders/', views.RecentOrderApiView.as_view(), name='recent-orders'),
    path('cancel_order/<int:pk>/',
         views.CancelOrderApiView.as_view(), name='cancel-order')
]
