from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Hashtag(models.Model):
    tag = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.tag)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField()
    image = models.ImageField(upload_to='posts_images/', blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="posts")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.creator.username} on {self.date_created.strftime('%Y-%m-%d %H:%M')}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username} on post {self.post.id}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_posts")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"Like by {self.user.username} on post {self.post.id}"

class Favorite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="favorites")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_posts")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"Favorite post {self.post.id} by {self.user.username}"

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    date_subscribed = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')

    def __str__(self):
        return f"{self.subscriber.username} subscribed to {self.subscribed_to.username}"