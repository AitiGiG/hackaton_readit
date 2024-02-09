from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, SubcategoryViewSet


router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'subcategory',SubcategoryViewSet, basename='subcategory')



urlpatterns = [
    path('', include(router.urls)),
]