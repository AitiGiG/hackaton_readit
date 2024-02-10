from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from .models import Hashtag, Post, Comment, Like, Favorite, Subscription
from .serializers import (
    HashtagSerializer,
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
    FavoriteSerializer,
    SubscriptionSerializer
)
from .permissions import IsOwnerOrReadOnly
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from googletrans import Translator, LANGUAGES
from django.http import JsonResponse
from .models import Comment
import logging  

logger = logging.getLogger('post')  

class HashtagListView(generics.ListCreateAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HashtagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        logger.info('New post created by user {}'.format(self.request.user))  # Логирование создания нового поста
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        logger.debug("Вызван метод list для PostListView")
        return super(PostListView, self).list(request, *args, **kwargs)
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id is not None:
            queryset = queryset.filter(author__id=user_id)
        return queryset


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.select_related('post').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post_id')
        if post_id is not None:
            queryset = queryset.filter(post__id=post_id)
        return queryset

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = get_object_or_404(Post.objects.prefetch_related('comments'), pk=post_id)
        serializer.save(commenter=self.request.user, post=post)
        logger.info('New comment created by user {} on post {}'.format(self.request.user, post))  # Логирование создания нового комментария

class CommentDestroyView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(commenter=user)

class LikeCreateDestroyView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info('User {} liked a post'.format(self.request.user))  # Логирование нажатия на кнопку "Лайк"
class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
class FavoriteCreateView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post)
        logger.info('User {} added post {} to favorites'.format(self.request.user, post))  # Логирование добавления поста в избранное

class FavoriteDestroyView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)

class SubscriptionListView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(subscriber=self.request.user)
        logger.info('User {} subscribed to a new user'.format(self.request.user))  # Логирование подписки на нового пользователя
class SubscriberListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer  
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):

        user_id = self.kwargs['user_id']
        return Subscription.objects.filter(subscribed_to__id=user_id)
class SubscriptionDestroyView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Subscription.objects.none()
        if isinstance(self.request.user, AnonymousUser):
            return Subscription.objects.none()
        return Subscription.objects.filter(subscriber=self.request.user)

class CustomLoginView(views.APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info('User {} logged in successfully'.format(username))  # Логирование успешного входа
            return Response({'success': True, 'message': 'Login successful'})
        else:
            logger.error('Invalid request method for login')  # Логирование недопустимого метода запроса
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'}, status=405)
    
def translate_comment(request, comment_id):
    if request.method == 'GET':

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found'}, status=404)

        translator = Translator()

        translated = translator.translate(comment.text, src='en', dest='ru')

        return JsonResponse({'original': comment.text, 'translated': translated.text})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)