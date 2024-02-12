from django.urls import path
from django.views.decorators.cache import cache_page
from apps.posts import views 
from .views import (
    HashtagListView,
    HashtagDetailView,
    PostListView,
    PostDetailView,
    CommentCreateView,
    CommentDestroyView,
    LikeCreateDestroyView,
    FavoriteCreateView,
    FavoriteDestroyView, 
    SubscriptionListView,
    SubscriptionDestroyView,
    CommentListView,
    FavoriteListView,
    SubscriberListView,
    FollowersListView,
    translate_comment,
    RecommendedPostsListView,
    PostCreateView,
)

app_name = 'apps.posts' 

urlpatterns = [
    path('hashtags/', HashtagListView.as_view(), name='hashtag-list'),
    path('hashtags/<int:pk>/', HashtagDetailView.as_view(), name='hashtag-detail'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/add/', PostCreateView.as_view(), name='post-create'), 
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/add/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', CommentDestroyView.as_view(), name='comment-destroy'),
    path('posts/<int:post_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('posts/comments/<int:comment_id>/translate/', translate_comment, name='translate-comment'),
    path('likes/toggle/', LikeCreateDestroyView.as_view(), name='like-create-destroy'),
    path('favorites/', FavoriteCreateView.as_view(), name='favorite-create'),
    path('favorites/list/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/<int:pk>/', FavoriteDestroyView.as_view(), name='favorite-destroy'),
    path('users/<int:user_id>/subscribers/', SubscriberListView.as_view(), name='subscriber-list'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription-list'),
    path('subscriptions/<int:pk>/', SubscriptionDestroyView.as_view(), name='subscription-destroy'),
    path('myfollowers/', FollowersListView.as_view(), name='my-followers-list'),
    path('login_view/', LikeCreateDestroyView.as_view(), name='login_view'),
    path('cashe_view/', cache_page(60 * 15)(PostListView.as_view()), name='cache_view'),
    path('recommended-posts/', RecommendedPostsListView.as_view(), name='recommended-posts'),
    
]