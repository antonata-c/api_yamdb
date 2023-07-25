from django.db import models
from django.core.validators import MaxValueValidator

from api.consts import (TEXT_LENGTH,
                        TITLES_NAMES_LENGTH,
                        USERNAME_SLUG_SHOW_LENGTH)
from api.validators import get_current_year


class NameSlugModel(models.Model):
    """Абстрактный класс для категорий и жанров."""

    name = models.CharField(max_length=TITLES_NAMES_LENGTH,
                            verbose_name='Название')
    slug = models.SlugField(max_length=USERNAME_SLUG_SHOW_LENGTH,
                            unique=True,
                            verbose_name='Слаг', )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Category(NameSlugModel):
    """Класс категорий произведений."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):
    """Класс жанров произведений."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField(max_length=TITLES_NAMES_LENGTH,
                            verbose_name='Название произведения')
    year = models.SmallIntegerField(
        db_index=True,
        verbose_name='Год выпуска',
        validators=(
            MaxValueValidator(get_current_year, 'В будущем произведения'
                                                ' неизвестны.'),
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
        return self.name[:TEXT_LENGTH]


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

    def __str__(self):
        return f'{self.title} относится к жанру {self.genre}'
