from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class User(AbstractUser):
    class Roles(models.TextChoices):
        MODERATOR = "moderator", "Модератор"
        ADMIN = "admin", "Администратор"
        USER = "user", "Пользователь"

    username = models.CharField(max_length=150, unique=True, blank=False,
                                validators=(RegexValidator(r'^[\w.@+-]+$',),))
    email = models.EmailField(max_length=254, unique=True, blank=False)
    first_name = models.TextField(max_length=150, blank=True)
    last_name = models.TextField(max_length=150, blank=True)

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.TextField(
        'Роль',
        blank=False,
        choices=Roles.choices,
        default=Roles.USER
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username[:settings.USERNAME_LENGTH]

    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    def is_admin(self):
        return self.role == self.Roles.ADMIN
