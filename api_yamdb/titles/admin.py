from django.contrib import admin

from .models import Title, Category, Genre
from reviews.models import Review, Comment


admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
