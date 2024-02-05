from django.db import models
from rest_framework.response import Response

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class HashTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.name.startswith('#'):
            return  Response('Хештег должен начинаться с символа "#".', 204)
        super(HashTag, self).save(*args, **kwargs)

class PostHashTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'hashtag')