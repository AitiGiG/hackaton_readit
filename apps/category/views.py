from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CategorySerializer, SubcategorySerializer
from .models import Category , Subcategory

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    @action(detail=False, methods=['GET'], url_path='(?P<slug>[-\w]+)')
    def get_category_by_slug(self, request, slug=None):
        try:
            category = Category.objects.get(slug=slug)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found"}, status=404)

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    @action(detail=False, methods=['GET'], url_path='(?P<slug>[-\w]+)')
    def get_subcategory_by_slug(self, request, slug=None):
        try:
            subcategory = Subcategory.objects.get(slug=slug)
            serializer = SubcategorySerializer(subcategory)
            return Response(serializer.data)
        except Subcategory.DoesNotExist:
            return Response({"detail": "Subcategory not found"}, status=404)