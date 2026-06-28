from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class TelegramMessage(models.Model):
    tg_login = models.ForeignKey("User", on_delete=models.CASCADE)
    user_text = models.TextField()
    chatbot_respond = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.tg_login)

class UserManager(BaseUserManager):
    def create_user(self, password=None, **extra_fields):
        if not any([extra_fields.get('email'), extra_fields.get('phone'), extra_fields.get('tg_login')]):
            raise ValueError('At least one of email, phone, or telegram_id is required')

        if extra_fields.get('email'):
            extra_fields['email'] = self.normalize_email(extra_fields['email'])

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(password=password, email=email, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    tg_login = models.CharField(max_length=32, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email or self.phone or str(self.tg_login)
