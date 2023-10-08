from rest_framework import serializers
from estore.models import Product,Brand,Category

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField(many=True)
    brand=serializers.StringRelatedField(many=True)
    class Meta:
        model = Product
        fields = '__all__'