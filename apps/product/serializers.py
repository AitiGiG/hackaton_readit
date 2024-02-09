from rest_framework.serializers import ModelSerializer
from .models import Product
from rest_framework import serializers
from .models import Category , Subcategory, Busket, Review, Favorite



class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'subcategory', 'price', 'description', 'image', 'quantity', 'available', 'favorites', 'owner', 'reviews']

    owner = serializers.ReadOnlyField(source='owner.email')
    favorites = serializers.SerializerMethodField(method_name='get_favorites_counter')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    def get_favorites_counter(self, instance):
        favorites_counter = instance.favorites.all().count()
        return favorites_counter
      
    def get_reviews(self, instance):
        reviews = instance.reviews.all()
        serializer = ReviewSerializer(
            reviews, many=True
        ) 
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.email')
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        exclude = ['created_at']
        model = Review

class BusketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    product = serializers.ReadOnlyField(source='product.title')
    quantity = serializers.IntegerField()
    class Meta:
        model = Busket
        fields = '__all__'
    
class FavoriteSerializer(serializers.Serializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    post = serializers.ReadOnlyField(source='product.title')

    class Meta:
        fields = '__all__'
        model = Favorite