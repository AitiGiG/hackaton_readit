from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

@api_view(['POST'])
def create_post(request):
    content = request.data.get('content', '')

    serializer = PostSerializer(data={'content': content})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def post_list(request, hashtag=None):
    if hashtag:
        posts = Post.objects.filter(hashtags__name=hashtag)
    else:
        posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def post_list_with_hashtag(request, hashtag):
    posts = Post.objects.filter(hashtags__name=hashtag)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
