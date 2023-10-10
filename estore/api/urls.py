from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListApiView.as_view(), name='product-list'),
    path('add-product/', views.ProductCreateApiView.as_view(), name='add-product'),
    path('categories/',views.CategoryApiView.as_view(), name='category-list'),
    path('products/<int:pk>/', views.ProductDetailApiView.as_view(),name='product-detail'),
    path('categories/<int:id>/', views.CategoryDetailApiView.as_view(),name='category-detail')
]