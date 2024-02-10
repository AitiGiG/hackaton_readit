from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import gettext_lazy as _
 

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            return ValueError('почта должна обяз передаваться')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_closed', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        return self._create_user(email, password, **kwargs)
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    activation_code = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=100)
    link = models.CharField(max_length=255, blank=True)
    biography = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='users_images', blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    objects = UserManager()
    last_username_change = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    last_online = models.DateTimeField(blank=True, null=True)

    def is_online(self):
        if self.last_online:
            return (timezone.now() - self.last_online) < timezone.timedelta(minutes=15)
        return False

    def get_online_info(self):
        if self.is_online():
            return _('Online')
        if self.last_online:
            return _('Last visit {}').format(naturaltime(self.last_online))
        return _('Unknown')
    
    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code
    
    def __str__(self) -> str:
        return self.email
    

    def can_change_username(self):
        if self.last_username_change:
            return timezone.now() - self.last_username_change > timezone.timedelta(days=30)
        return True

    def update_username(self, new_username):
        self.username = new_username
        self.last_username_change = timezone.now()
        self.save()


