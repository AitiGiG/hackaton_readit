from django.urls import path
from .views import create_post, post_list, post_list_with_hashtag

# urlpatterns = [
#     path('posts/', create_post, name='create_post'),  
#     path('posts/<str:hashtag>/', post_list, name='post_list_with_hashtag'),
#     path('posts/', post_list, name='post_list'),
# ]

urlpatterns = [
    path('posts/create/', create_post, name='create_post'),  
    path('posts/<str:hashtag>/', post_list_with_hashtag, name='post_list_with_hashtag'),
    path('posts/', post_list, name='post_list'),
]
