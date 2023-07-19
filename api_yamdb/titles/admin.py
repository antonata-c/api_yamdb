from django.contrib import admin

from .models import Title, Category, Genre
from reviews.models import Review, Comment


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year',
                    'description', 'get_genres', 'category')
    list_display_links = ('name', 'get_genres', 'category')

    @admin.display(description='Жанр')
    def get_genres(self, obj):
        return ", ".join([str(p) for p in obj.genre.all()])


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name', 'slug')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'title', 'author', 'pub_date', 'score')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date', 'review')
