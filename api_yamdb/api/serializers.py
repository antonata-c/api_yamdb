from django.core.validators import MaxValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from .consts import NAME_LENGTH, USERNAME_SLUG_SHOW_LENGTH, EMAIL_LENGTH
from .validators import username_validator, get_current_year
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
        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        )

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

    def create(self, validated_data):
        found_user, created = User.objects.get_or_create(
            **validated_data
        )
        if not created:
            return validated_data
        return found_user

    def validate(self, data):
        if not all((User.objects.filter(username=data.get('username')),
                    User.objects.filter(email=data.get('email')))):
            if User.objects.filter(username=data.get('username')):
                raise serializers.ValidationError(
                    'Имя пользователя уже занято!')
            if User.objects.filter(email=data.get('email')):
                raise serializers.ValidationError('Email уже занят!')
        return data


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
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(title=title_id,
                                     author=request.user).exists():
                raise ValidationError('Вы не можете добавить более одного '
                                      'отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
