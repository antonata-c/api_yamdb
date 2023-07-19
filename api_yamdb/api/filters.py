import django_filters as df

from titles.models import Title


class TitleFilter(df.FilterSet):
    """Фильтры произведений."""

    name = df.CharFilter(field_name='name',
                         lookup_expr='icontains',
                         label='Название')
    category = df.CharFilter(field_name='category__slug',
                             lookup_expr='icontains',
                             label='Категория')
    genre = df.CharFilter(field_name='genre__slug',
                          lookup_expr='icontains',
                          label='Жанр')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')
