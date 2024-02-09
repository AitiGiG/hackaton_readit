from rest_framework import serializers
from .models import Category, Subcategory

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'
    category = serializers.StringRelatedField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'slug') 
    