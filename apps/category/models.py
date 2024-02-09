from django.db import models
from autoslug import AutoSlugField


class Category(models.Model):
    CATEGORY_CHOICES = (
        ('dress', 'Одежда'),
        ('electronics', 'Электроника'),
        ('furniture', 'Мебель'),
        ('books', 'Книги'), 
    )
    title = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)

    def __str__(self):
        return self.title
class Subcategory(models.Model):
    title = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.title