"""Проект спринта 10: модуль сериалайзер приложения Api."""
import datetime
import re

from django.conf import settings
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title


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
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        return rating if not rating else round(rating, 0)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category',)
        model = Title
        read_only_fields = ('id', 'pub_date', 'rating',)


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

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', )
        model = Title
        read_only_fields = ('id', 'pub_date',)
        validators = (
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'genre'),
                message=('Запрещено присваивать повторные жанры')
            ),
        )

    def validate_year(self, value):
        """Год выпуска не может быть больше текущего."""
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего"
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для Review."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')
    title = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST' and Review.objects.filter(
            title=title, author=author
        ).exists()):
            raise ValidationError(
                f"Пользователь {author.username} уже оставил отзыв к "
                f"произведению {title.name}")
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')
    review = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Создадим сериалайзер для регистрации пользователей"""

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = CustomUser


class UserEditSerializer(serializers.ModelSerializer):
    """Сериалайзер для самостоятельного редактирования пользователей"""

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = CustomUser
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации пользователей"""
    username = serializers.CharField(
        max_length=settings.MAX_LENGHT_USERNAME,
        required=True,
    )
    email = serializers.EmailField(
        max_length=settings.MAX_LENGHT_EMAIL,
        required=True,
    )

    def validate_username(self, value):
        """Проверим указанное имя пользователя"""
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' не валидно")
        if not re.fullmatch(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                r'username не соответствует паттерну: ^[\w.@+-]+\Z'
            )
        return value

    class Meta:
        fields = ("username", "email")
        model = CustomUser


class TokenSerializer(serializers.Serializer):
    """Создадим сериалайзер для получения JWT-токена"""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
