from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = models.CharField(max_length=30, verbose_name='Имя пользователя', **NULLABLE)
    phone = models.CharField(max_length=30, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')

    is_active = models.BooleanField(default=False, verbose_name='активность')
    user_token = models.CharField(max_length=255, blank=True, null=True, verbose_name='токен')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        permissions = [
            ('set_active',
             'блокировка/активный')
        ]

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'