from django.contrib.auth.models import AbstractUser
from django.db import models

from api.consts import NAME_LENGTH, EMAIL_LENGTH, USERNAME_SLUG_SHOW_LENGTH
from api.validators import username_validator


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = (
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь')
    )
    username = models.CharField(max_length=NAME_LENGTH, unique=True,
                                blank=False,
                                validators=(username_validator,))
    email = models.EmailField(max_length=EMAIL_LENGTH, unique=True,
                              blank=False)
    first_name = models.TextField(max_length=NAME_LENGTH, blank=True)
    last_name = models.TextField(max_length=NAME_LENGTH, blank=True)

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.TextField(
        'Роль',
        blank=False,
        choices=ROLES,
        default=USER,
        max_length=max(len(role) for role, _ in ROLES)
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:USERNAME_SLUG_SHOW_LENGTH]

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser
