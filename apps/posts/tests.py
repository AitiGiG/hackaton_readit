from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from apps.posts.models import Post, Hashtag
from apps.posts.views import PostListView
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class PostTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = self.setUp_user()
        self.token = self.setUp_user_token()
        self.setUp_hashtag()
        self.setUp_post()

    def setUp_user(self):
        return User.objects.create_superuser(email='test@gmail.com', password='1')
    
    def setUp_user_token(self):
        data = {
            "email": "test@gmail.com",
            "password": "1" 
        }
        request = self.factory.post('account/login/', data)  
        view = TokenObtainPairView.as_view()  
        response = view(request) 
        # print(response.data)  
        return response.data['access'] 

    def setUp_hashtag(self):
        hashtags = [
            Hashtag.objects.create(tag='tag1'), 
            Hashtag.objects.create(tag='tag2'), 
            Hashtag.objects.create(tag='tag3'), 
        ]

    def setUp_post(self):
        posts = [
            Post(creator=self.user, description='description1'), 
            Post(creator=self.user, description='description2'), 
            Post(creator=self.user, description='description3'), 
        ]
        Post.objects.bulk_create(posts)

    def test_get_post(self):
        request = self.factory.get('post/')
        view = PostListView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, 200)

    def test_post_post(self):
        data = {
            'description': 'test_post',
            'hashtags': [hashtag.pk for hashtag in Hashtag.objects.all()],
            'date_created': '2022-01-01'
        }
        request = self.factory.post('posts/posts/', data, HTTP_AUTHORIZATION='Bearer '+self.token)
        view = PostListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 201)