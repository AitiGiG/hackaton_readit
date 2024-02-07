from rest_framework import serializers
from .models import Hashtag, Post, Comment, Like, Favorite, Subscription, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'tag', 'slug']

class PostSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'creator', 'description', 'image', 'hashtags', 'date_created']

class CommentSerializer(serializers.ModelSerializer):
    commenter = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'commenter', 'content', 'date_created']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'date_created']

class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'post', 'user', 'date_added']

class SubscriptionSerializer(serializers.ModelSerializer):
    subscriber = UserSerializer(read_only=True)
    subscribed_to = UserSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'subscriber', 'subscribed_to', 'date_subscribed']