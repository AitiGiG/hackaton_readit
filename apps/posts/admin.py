from django.contrib import admin
from .models import Hashtag, Post, Comment, Like, Favorite, Subscription

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'slug')
    search_fields = ('tag',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('description', 'creator', 'date_created')
    search_fields = ('description', 'creator__username')
    list_filter = ('date_created', 'hashtags',)
    date_hierarchy = 'date_created'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'commenter', 'post', 'date_created')
    search_fields = ('content', 'commenter__username', 'post__description')
    list_filter = ('date_created',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'date_created')
    search_fields = ('post__description', 'user__username')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'date_added')
    search_fields = ('post__description', 'user__username')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed_to', 'date_subscribed')
    search_fields = ('subscriber__username', 'subscribed_to__username')