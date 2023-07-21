from rest_framework import filters, mixins, viewsets

from .permissions import ReadOnly, IsAdmin


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьсет для get, post, delete запросов."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (ReadOnly | IsAdmin,)
