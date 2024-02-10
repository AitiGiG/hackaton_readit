from rest_framework import viewsets, permissions, views, status, generics
from rest_framework.response import Response
from .models import GamePassport, PostGame, GameLike, GameComment, Activity, ActivityParticipation
from .serializers import (
    GamePassportSerializer, PostGameSerializer, 
    GameCommentSerializer, ActivitySerializer
)
from .permissions import IsOwnerOrReadOnly, IsActivityCreator

class GamePassportViewSet(viewsets.ModelViewSet):
    queryset = GamePassport.objects.all()
    serializer_class = GamePassportSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostGameViewSet(viewsets.ModelViewSet):
    queryset = PostGame.objects.all()
    serializer_class = PostGameSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        passport = self.request.user.game_passport
        serializer.save(passport=passport)

class GameLikeCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        user = request.user
        if not GameLike.objects.filter(post_id=post_id, user=user).exists():
            GameLike.objects.create(post_id=post_id, user=user)
            return Response({'status': 'like added'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)

class GameCommentCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        text = request.data.get('text', '')
        user = request.user
        try:
            post = PostGame.objects.get(id=post_id)  
        except PostGame.DoesNotExist:
            return Response({'status': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        GameComment.objects.create(post=post, user=user, text=text)
        return Response({'status': 'comment added'}, status=status.HTTP_201_CREATED)

class PostGameCommentsListView(generics.ListAPIView):
    serializer_class = GameCommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return GameComment.objects.filter(post__id=post_id)

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated, IsActivityCreator]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ActivityParticipationView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        activity_id = kwargs.get('activity_id')
        is_ready = request.data.get('is_ready', True)
        user = request.user
        try:
            activity = Activity.objects.get(id=activity_id)
        except Activity.DoesNotExist:
            return Response({'status': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)

        ActivityParticipation.objects.update_or_create(
            activity=activity, participant=user, defaults={'is_ready': is_ready}
        )
        return Response({'status': 'participation status updated'}, status=status.HTTP_200_OK)