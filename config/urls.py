from django.contrib import admin
from django.urls import path , include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="READIT",

        description="online backend api's for readit",

        default_version="v1",
    ),
    public=True
)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/swagger/', schema_view.with_ui('swagger')),
    path('api/account/', include('apps.account.urls')), 
    path('api/', include('apps.posts.urls', namespace='apps.posts')),
    path('api/', include('apps.product.urls')),
    path('api/', include('apps.category.urls')),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)