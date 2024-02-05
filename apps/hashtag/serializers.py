from rest_framework import serializers
from .models import Post, HashTag

class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ['name']

class PostSerializer(serializers.ModelSerializer):
    hashtags = HashTagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['content', 'created_at', 'hashtags']

    def create(self, validated_data):
        content = validated_data.get('content')
        hashtags = [tag.strip("#") for tag in content.split() if tag.startswith("#")]

        post = Post.objects.create(content=content)

        for tag in hashtags:
            hashtag, created = HashTag.objects.get_or_create(name=tag)
            post.hashtags.add(hashtag)

        return post

# from rest_framework import serializers
# from .models import Group, Post, Tag, TagPost

# class TagSerializer(serializers.ModelSerializer):

#     class Meta:
#         fields = ('name', )
#         model = Tag
    
# class PostSerializer(serializers.ModelSerializer):
#     group = serializers.SlugRelatedField(slug_field='slug', queryset=Group.objects.all(), required=False)
#     tag = TagSerializer(required=False, many=True)
#     class Meta:
#         fields = ('id', 'text', 'author', 'image', 'pub_date', 'group', 'tag')
#         model = Post
#     def create(self, validated_data):
#         if 'tag' not in self.initial_data:
            
#             post=Post.objects.create(**validated_data)
#             return post
#         else:
#             tag=validated_data.pop('tag')
#             post=Post.objects.create(**validated_data)
            
#             for one_tag in tag:
#                 current_tag, status = Tag.objects.get_or_create(**one_tag)
#                 TagPost.objects.create(tag=current_tag, post=post)
#             return post