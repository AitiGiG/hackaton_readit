from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
from apps.product.models import Product, Busket, Favorite
from apps.product.serializers import ProductSerializer, BusketSerializer, FavoriteSerializer
from apps.posts.serializers import SubscriptionSerializer
from apps.posts.models import Subscription


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'id','email', 'password', 'password_confirm','username'
        ]

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Passwords do not match!')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'biography', 'avatar', 'link', 'is_closed', 'is_staff',  'last_online']

class UserGetProductSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'busket', 'favorite', 'last_online', 'my_subscribers', 'im_subscribed']
    
    busket = serializers.SerializerMethodField(method_name='get_busket')
    favorite = serializers.SerializerMethodField(method_name='get_favorite')
    my_subscribers = serializers.SerializerMethodField(method_name='get_my_subscribers')
    im_subscribed = serializers.SerializerMethodField(method_name='get_im_subscribed')
    
    def get_busket(self , instance):
        busket = Busket.objects.filter(owner=instance)
        serializer = BusketSerializer(busket, many=True)
        return serializer.data
    def get_favorite(self, instance):
        favorite = Favorite.objects.filter(owner=instance)
        serializer = FavoriteSerializer(favorite, many=True)
        return serializer.data
    
    def get_my_subscribers(self, instance):
        subscriptions = Subscription.objects.filter(subscriber=instance)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return serializer.data
    def get_im_subscribed(self, instance):
        subscriptions = Subscription.objects.filter(subscribed_to=instance)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return serializer.data
    
class UserVipGetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_staff', 'product','last_online']
    
    product= serializers.SerializerMethodField(method_name='get_product')

    def get_product(self, instance):
        product = Product.objects.filter(owner=instance)
        serializer = ProductSerializer(product, many=True)
        return serializer.data