from django.urls import path
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
)

app_name = 'apps.posts' 

urlpatterns = [
    path('hashtags/', HashtagListView.as_view(), name='hashtag-list'),
    path('hashtags/<int:pk>/', HashtagDetailView.as_view(), name='hashtag-detail'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', CommentDestroyView.as_view(), name='comment-destroy'),
    path('likes/', LikeCreateDestroyView.as_view(), name='like-create-destroy'),
    path('favorites/', FavoriteCreateView.as_view(), name='favorite-create'),
    path('favorites/<int:pk>/', FavoriteDestroyView.as_view(), name='favorite-destroy'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription-list'),
    path('subscriptions/<int:pk>/', SubscriptionDestroyView.as_view(), name='subscription-destroy'),
]