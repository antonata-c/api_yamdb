import datetime

from django.db import models
from django.conf import settings
from django.core.validators import (MaxValueValidator,
                                    RegexValidator,
                                    MinValueValidator)


class Category(models.Model):
    """Класс категорий произведений."""

    name = models.CharField(max_length=256,
                            verbose_name='Название категории')
    slug = models.CharField(max_length=50,
                            unique=True,
                            verbose_name='Слаг категории',
                            validators=(RegexValidator('^[-a-zA-Z0-9_]+$',),))

    class Meta:
        verbose_name = 'Категория произведения'
        verbose_name_plural = 'Категории произведений'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.TEXT_LENGTH]


class Genre(models.Model):
    """Класс жанров произведений."""

    name = models.CharField(max_length=256,
                            verbose_name='Название жанра')
    slug = models.CharField(max_length=50,
                            unique=True,
                            verbose_name='Слаг жанра',
                            validators=(RegexValidator('^[-a-zA-Z0-9_]+$',),))

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.TEXT_LENGTH]


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(datetime.datetime.now().year),
        )
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='title',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        related_name='title',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)

    def __str__(self):
        return self.name[:settings.TEXT_LENGTH]


class GenreTitle(models.Model):
    """Класс модели для связи жанров и произведений."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Связь жанра и произведения'
        verbose_name_plural = 'Связи жанров и произведений'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} относится к жанру {self.genre}'
