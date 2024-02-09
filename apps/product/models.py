from django.db import models
from apps.category.models import Category, Subcategory
from django.contrib.auth import get_user_model

User = get_user_model()
class Product(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='products',
    )
    subcategory = models.ForeignKey(
        Subcategory, 
        on_delete=models.CASCADE,
        related_name='products',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product_images', blank=True)
    quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.available = False
        else:
            self.available = True
        super().save(*args, **kwargs)


class Busket(models.Model):
    owner = models.ForeignKey(User, related_name='buskets', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='buskets', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Корзина для {self.owner.email} | Продукт: {self.product.title}'

# Create your models here.

class Review(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    created_at = models.DateField(auto_now_add=True)
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='reviews'
    )
class Favorite(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        User,
        related_name='favorite_owners',
        on_delete=models.CASCADE
    )

