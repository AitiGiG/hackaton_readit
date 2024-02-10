from django.urls import path
from .views import (
    GamePassportViewSet, 
    PostGameViewSet, 
    GameLikeCreateView, 
    GameCommentCreateView, 
    ActivityViewSet, 
    ActivityParticipationView,
    PostGameCommentsListView,
)

app_name = 'apps.game_pasport' 

urlpatterns = [
    path('gamepassport/', GamePassportViewSet.as_view({'get': 'list', 'post': 'create'}), name='gamepassport-list'),
    path('gamepassport/<int:pk>/', GamePassportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='gamepassport-detail'),
    path('postgame/', PostGameViewSet.as_view({'get': 'list', 'post': 'create'}), name='postgame-list'),
    path('postgame/<int:pk>/', PostGameViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='postgame-detail'),
    path('postgame/<int:post_id>/like/', GameLikeCreateView.as_view(), name='postgame-like'),
    path('postgame/<int:post_id>/comment/', GameCommentCreateView.as_view(), name='postgame-comment'),
    path('postgame/<int:post_id>/comments/', PostGameCommentsListView.as_view(), name='postgame-comments-list'),
    path('activity/', ActivityViewSet.as_view({'get': 'list', 'post': 'create'}), name='activity-list'),
    path('activity/<int:pk>/', ActivityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='activity-detail'),
    path('activity/<int:activity_id>/participate/', ActivityParticipationView.as_view(), name='activity-participate'),
]