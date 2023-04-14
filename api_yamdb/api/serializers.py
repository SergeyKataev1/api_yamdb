"""Проект спринта 10: модуль сериалайзер приложения Api."""
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import (
    UniqueTogetherValidator,
    UniqueValidator, ValidationError
)
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title
from reviews.validators import model_validate_username, model_validate_year


class CategorySerializer(serializers.ModelSerializer):
    """Класс-сериализатор для Category."""

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для Genre."""

    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleGetSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для Titles."""
    genre = GenreSerializer(
        many=True
    )
    category = CategorySerializer()
    rating = serializers.IntegerField(default=0)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category',)
        model = Title
        read_only_fields = fields


class TitleSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для Titles."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    year = serializers.IntegerField(validators=[model_validate_year, ])

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')
        model = Title
        validators = (
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'genre'),
                message=('Запрещено присваивать повторные жанры')
            ),
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для Review."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')
    title_id = serializers.IntegerField(read_only=True, )

    class Meta:
        model = Review
        fields = ('id', 'author', 'title_id', 'text', 'score', 'pub_date',)
        read_only_fields = ('id', 'author', 'title', 'pub_date',)

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST' and Review.objects.filter(
                title=get_object_or_404(
                    Title,
                    pk=self.context['view'].kwargs['title_id']),
                author=request.user
        ).exists():
            raise ValidationError(
                f"Пользователь {request.user.username} "
                "уже оставил отзыв к произведению.")
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')
    review_id = serializers.IntegerField(read_only=True, )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'review_id', 'text', 'pub_date',)
        read_only_fields = ['id', 'author', 'review_id', 'pub_date', ]


class UserSerializer(serializers.ModelSerializer):
    """Создадим сериалайзер для регистрации пользователей"""
    username = serializers.CharField(
        max_length=settings.MAX_LENGTH_USERNAME,
        required=True,
        # При переносе валидатора в общий валидатор или валидатор поля возникают ошибки pytest:
        # >       return Database.Cursor.execute(self, query, params)
        # E       sqlite3.IntegrityError: UNIQUE constraint failed: reviews_customuser.username
        # или
        # E       AssertionError: Проверьте, что при обработке POST-запроса к `/api/v1/users/` содержание поля `username` проверяется на соответствие паттерну, указанному в спецификации: ^[\w.@+-]+\z
        # E       assert 201 == <HTTPStatus.BAD_REQUEST: 400>
        # E         +201
        # E         -<HTTPStatus.BAD_REQUEST: 400>
        validators=(
            UniqueValidator(queryset=CustomUser.objects.all()),
            model_validate_username,
        ),
    )

    # def validate_username(self, value):
    #     model_validate_username(value)
    #     return value

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role",)
        model = CustomUser


class UserEditSerializer(serializers.ModelSerializer):
    """Сериалайзер для самостоятельного редактирования пользователей"""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.Serializer):
    """Сериалайзер для регистрации пользователей"""
    username = serializers.CharField(
        max_length=settings.MAX_LENGTH_USERNAME,
        required=True,
        validators=[model_validate_username, ]
    )
    email = serializers.EmailField(
        max_length=settings.MAX_LENGTH_EMAIL,
        required=True,
    )

    # !!! без этого метода возникает массовая ошибка pytest
    # > raise NotImplementedError('`create()` must be implemented.')
    # E NotImplementedError: `create()` must be implemented.
    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    class Meta:
        fields = ("username", "email")
        model = CustomUser


class TokenSerializer(serializers.Serializer):
    """Создадим сериалайзер для получения JWT-токена"""
    username = serializers.CharField(
        max_length=settings.MAX_LENGTH_USERNAME,
        required=True,
        validators=(model_validate_username,)
    )
    confirmation_code = serializers.CharField(
        required=True, max_length=settings.MAX_CONFIRMATION_CODE
    )
