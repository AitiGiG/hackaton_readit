from django.contrib import admin
from django.urls import path , include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView
from apps.posts.views import PostListView
from apps.posts.views import PostListView

schema_view = get_schema_view(
   openapi.Info(
      title="READIT",
      default_version='v1',
      description="online backend api's for shop",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourdomain.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)


urlpatterns = [
    path('cache/', PostListView.as_view(), name='cache'),
    path('admin/', admin.site.urls),  
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  
    path('account/', include('apps.account.urls')), 
    path('posts/', include('apps.posts.urls', namespace='apps.posts')), 
    path('product/', include('apps.product.urls')),
    path('category/', include('apps.category.urls')),
    path('gamepassport/', include('apps.game_passport.urls', namespace='apps.game_passport')),  
    path('chat/', include('apps.chat.urls', namespace='apps.chat'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)