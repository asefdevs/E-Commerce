from rest_framework.views import APIView
from .serializers import ProductListSerializer,CategoryListSerializer,ProductDetailSerializer,CategoryDetailSerializer
from estore.models import Product,Category
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import NotFound
from .permissions import IsAdminorReadOnly
from django.shortcuts import get_object_or_404
class ProductApiView(generics.ListCreateAPIView):
    queryset=Product.objects.filter(is_active=True)
    serializer_class=ProductListSerializer
    # permission_classes=[IsAdminorReadOnly]

class CategoryApiView(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategoryListSerializer
    # permission_classes=[IsAdminorReadOnly]

class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductDetailSerializer
    # permission_classes=[IsAdminorReadOnly]

class CategoryDetailApiView(APIView):
    def get(self,request,id):
        products=Product.objects.filter(catogory__id=id)
        serializer=ProductDetailSerializer(products,many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)


