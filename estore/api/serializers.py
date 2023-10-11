from rest_framework import serializers
from estore.models import Product, Category


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['name']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'category',
            'image',
            'brand',
            'stock_quantity',
            'size',
            'color',
            'created_at',
            'updated_at',
        ]
class ProductListSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'category',
            'image',
            'brand',
            'stock_quantity',
            'size',
            'color',
            'created_at',
            'updated_at',
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Product
        fields='__all__'