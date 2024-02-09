from django.contrib import admin
from django.urls import path , include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView
from apps.posts.views import PostListView
from rest_framework_swagger.views import get_swagger_view
from apps.posts.views import PostListView


schema_view = get_schema_view(
    openapi.Info(
        title="READIT",

        description="online backend api's for readit",


# schema_view = get_schema_view(
#     openapi.Info(
#         title="SHOP API",

#         description="online backend api's for shop",

#         default_version="v1",
#     ),
#     public=True
# )

# app_name = 'posts'
schema_view = get_swagger_view(title='API')

schema_view = get_schema_view(
   openapi.Info(
      title="SHOP API",
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
    path('api/admin/', admin.site.urls),
    path('api/swagger/', schema_view.with_ui('swagger')),
    path('api/account/', include('apps.account.urls')), 
    path('api/', include('apps.posts.urls', namespace='apps.posts')),
    path('api/', include('apps.product.urls')),
    path('api/', include('apps.category.urls')),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)