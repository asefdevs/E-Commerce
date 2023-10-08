from rest_framework.views import APIView
from .serializers import ProductSerializer,CategorySerializer,BrandSerializer
from estore.models import Product,Category,Brand
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import NotFound
from .permissions import IsAdminorReadOnly


class ProductApiView(generics.ListCreateAPIView):
    queryset=Product.objects.filter(is_active=True)
    serializer_class=ProductSerializer
    permission_classes=[IsAdminorReadOnly]
