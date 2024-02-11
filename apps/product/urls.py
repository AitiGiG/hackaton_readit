from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ActionsViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'product', ActionsViewSet, basename='product')


urlpatterns = [
    path('', include(router.urls)),
]