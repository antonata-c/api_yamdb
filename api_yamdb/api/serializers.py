from django.core.validators import MaxValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .consts import NAME_LENGTH, USERNAME_SLUG_SHOW_LENGTH, EMAIL_LENGTH
from .utils import get_current_year
from .validators import username_validator
from titles.models import Title, Category, Genre
from reviews.models import Review, Comment
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для безопасных методов."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для небезопасных методов."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    year = serializers.IntegerField(
        validators=(MaxValueValidator(get_current_year),)
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_genre(self, genre):
        if not genre:
            raise serializers.ValidationError('Для произведения '
                                              'жанры обязательны!')
        return genre

    def to_representation(self, title):
        return TitleSerializer(title).data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')
        model = User

    def validate(self, data):
        if (User.objects.filter(username=data.get('username'))
                and not User.objects.filter(email=data.get('email'))):
            raise serializers.ValidationError('Имя пользователя уже занято!')
        if (User.objects.filter(email=data.get('email'))
                and not User.objects.filter(username=data.get('username'))):
            raise serializers.ValidationError('Email уже занят!')
        return data

    def validate_username(self, username):
        return username_validator(username)


class TokenSerializer(serializers.Serializer):
    """Сериализатор токенов пользователей."""

    username = serializers.CharField(
        max_length=NAME_LENGTH,
        required=True,
        validators=(username_validator,),
    )
    confirmation_code = serializers.CharField(
        max_length=USERNAME_SLUG_SHOW_LENGTH,
        required=True
    )


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для подтверждения пользователя."""

    username = serializers.CharField(
        max_length=NAME_LENGTH,
        required=True,
        validators=(username_validator,),
    )
    email = serializers.EmailField(max_length=EMAIL_LENGTH, required=True)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        """Валидация на повторные отзывы."""
        request = self.context.get('request')
        if request.method == 'POST':
            author = request.user
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(title=title_id,
                                     author=author).exists():
                raise ValidationError('Вы не можете добавить более одного '
                                      'отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
