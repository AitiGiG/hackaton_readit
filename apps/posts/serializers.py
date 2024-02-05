from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'image', 'price', 'count', 'created_at', 'updated_at']
        read_only_fields = ['user']