from http import HTTPStatus

from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import (IsAdmin, ReadOnly, IsAdminModeratorOwnerOrReadOnly)
from .serializers import (TitleSerializer, CategorySerializer,
                          GenreSerializer, TitleCreateSerializer,
                          SignUpSerializer, TokenSerializer,
                          UserSerializer, CommentSerializer, ReviewSerializer)
from .utils import send_letter
from titles.models import Title, Category, Genre
from users.models import User
from reviews.models import Review


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (ReadOnly | IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('name', 'year', 'rating')
    ordering = ['name']
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        """Метод для определения класса сериализатора."""
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleCreateSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для изменения и удаления пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
        else:
            serializer = UserSerializer(request.user,
                                        data=request.data,
                                        partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=HTTPStatus.OK)


@api_view(["POST"])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    found_user, created = User.objects.get_or_create(
        **serializer.validated_data
    )
    confirmation_code = default_token_generator.make_token(found_user)

    send_letter(found_user.email, confirmation_code)
    return Response(serializer.validated_data, status=HTTPStatus.OK)


@api_view(["POST"])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data.get('username'))
    if not default_token_generator.check_token(
            user, request.data.get('confirmation_code')
    ):
        return Response({'confirmation_code': 'Введеный токен неверен!'},
                        status=HTTPStatus.BAD_REQUEST)
    return Response(
        {'token': str(AccessToken.for_user(user))},
        status=HTTPStatus.OK
    )


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminModeratorOwnerOrReadOnly)

    def get_queryset(self):
        """Метод для получения queryset с отзывами."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Метод для сохранения отзыва с автором текущего пользователя."""
        serializer.save(author=self.request.user, title=self.get_title())

    def get_title(self):
        """Метод для получения объекта Title."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        """Метод для получения queryset с комментариями."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Метод для сохранения комментария с автором текущего пользователя."""
        serializer.save(author=self.request.user, review=self.get_review())

    def get_review(self):
        """Метод для получения объекта Review."""
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))
