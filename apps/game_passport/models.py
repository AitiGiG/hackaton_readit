from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class GamePassport(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='game_passport')
    nickname = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='game_passport_avatars/', blank=True)
    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('trans', 'Transgender')
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    platforms = models.ManyToManyField(Platform)
    experience_years = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.nickname

class PostGame(models.Model):
    passport = models.ForeignKey(GamePassport, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='postgame_images/', blank=True)
    text = models.TextField()

    def __str__(self):
        return f'Post by {self.passport.nickname}'

class GameLike(models.Model):
    post = models.ForeignKey(PostGame, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'Like by {self.user.username} on {self.post.id}'

class GameComment(models.Model):
    post = models.ForeignKey(PostGame, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.id}'

class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_activities')
    participants = models.ManyToManyField(User, through='ActivityParticipation', related_name='joined_activities')
    selected_participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='selected_activities')

    def __str__(self):
        return self.title

class ActivityParticipation(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    is_ready = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.participant.username} participation in {self.activity.title}'