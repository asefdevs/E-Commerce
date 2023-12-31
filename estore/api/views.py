from rest_framework.views import APIView
from .serializers import ProductListSerializer, ProductCreateSerializer, CategoryListSerializer, ProductDetailSerializer
from estore.models import Product, Category
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .permissions import IsAdminorReadOnly
from .pagination import ProductPagination
from estore.filters import ProductFilter
from django_filters import rest_framework as filters


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = ProductPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


class ProductCreateApiView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminorReadOnly]


class CategoryApiView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [IsAdminorReadOnly]


class CategoryDetailApiView(APIView):
    def get(self, request, id):
        products = Product.objects.filter(category__id=id, is_active=True)
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
