from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductApiView.as_view(), name='product-list'),
    path('categories/',views.CategoryApiView.as_view(), name='category-list'),
    path('products/<int:pk>/', views.ProductDetailApiView.as_view(),name='product-detail')
]