from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import ReviewSerializer
from .tasks import send_purchase_email, send_review_notification_email
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import logging
from apps.category.models import Category
from apps.category.serializers import CategorySerializer
from .permissions import IsOwner


logger = logging.getLogger('product')

class StandartResultPagination(PageNumberPagination):
    page_size = 10
    page_query_param= 'page'

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandartResultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'category__title', 'subcategory__title', 'description']
    filersets_fields = ['category']
    
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsAdminUser()]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwner()] 
        return [permissions.IsAuthenticated()]  

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @method_decorator(cache_page(60*15))
    def list(self, request, *args, **kwargs):
        logger.debug("Вызван метод list для ProductViewSet")
        return super(ProductViewSet, self).list(request, *args, **kwargs)
        
    
    @action(detail=False, methods=['GET'], url_path='by_category/(?P<category_slug>[-\w]+)')
    def get_products_by_category_slug(self, request, category_slug=None):
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found"}, status=404)

        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    

class ActionsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def toggle_favorite(self, request, pk=None):
        product = self.get_object()
    
    # Проверяем, добавил ли пользователь товар в избранное
        favorite_exists = Favorite.objects.filter(product=product, owner=request.user).exists()

        if favorite_exists:
            # Если товар уже в избранном, удаляем его оттуда
            Favorite.objects.filter(product=product, owner=request.user).delete()
            return Response('Успешно удалено', status=204)
        else:
            # Если товар не в избранном, добавляем его
            favorite = Favorite.objects.create(product=product, owner=request.user)
            favorite.save()
            return Response('Успешно добавлено', status=201)


    @action (detail=True, methods=['POST', 'DELETE'])
    def add_busket(self, request, pk=None):
        product = self.get_object()
        busket_exists = Busket.objects.filter(product=product, owner=request.user).exists()
        if request.method == 'DELETE':
            Busket.objects.filter(product=product, owner=request.user).delete()
            return Response('Товар удален из корзины', status=204)
        
        if busket_exists:
            return Response('Товар уже в корзине', status=400)
            return Response('Количество не может быть отрицательным', status=400)
        else:
            busket = Busket.objects.create(product=product, owner=request.user , quantity=request.data['quantity'] if request.data['quantity'] else 1)
            busket.save()
            return Response('Товар добавлен в корзину', status=201)


    @action(detail=True, methods=['POST'])
    def buy_product(self, request, pk=None):
        product = self.get_object()
        busket = Busket.objects.get(product=product, owner=request.user)
        Product.objects.filter(id=product.id).update(quantity=product.quantity - int(busket.quantity))

        send_purchase_email.delay(
            owner_email=product.owner.email, 
            product_name=product.title, 
            quantity= busket.quantity,  
            buyer_username=request.user.username
        )

        Busket.objects.filter(product=product, owner=request.user).delete()
        return Response('Товар куплен', status=201)


    @action(detail=True, methods=['POST', 'DELETE'])
    def review(self, request, pk=None):
        product = self.get_object()
        if request.method == 'DELETE':
            res = Review.objects.filter(product=product, owner=request.user).delete()
            return Response(f'успешно удален', 204)
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product, owner=request.user)
        try:
            send_review_notification_email.delay(
            product_owner_email=product.owner.email,
            reviewer_username=request.user.username,
            product_title=product.title,
            review_content=request.data['content']
            )
        except Exception as e:
            return Response(
                {'error': f'Ошибка при отправке подтверждения по электронной почте: {e}'}
            )

        return Response('успешно добавлен', 201)
    
    