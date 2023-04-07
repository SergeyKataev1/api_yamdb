"""Проект спринта 10: модуль сериалайзер приложения Api."""
import datetime
import re

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from reviews.models import CustomUser


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

    def validate_username(self, value):
        """Проверяем username на соответствие паттерну."""
        if not re.fullmatch(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'username не соответствует паттерну: ^[\w.@+-]+\Z'
            )
        return value

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = CustomUser


class UserEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = CustomUser
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    def validate_username(self, value):
        """Проверим указанное имя пользователя"""
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' не валидно")
        if not re.fullmatch(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'username не соответствует паттерну: ^[\w.@+-]+\Z'
            )
        if (
            CustomUser.objects.filter(username=value).exists()
            and not CustomUser.objects.filter(
                email=self.initial_data.get('email')
            ).exists()
        ):
            raise serializers.ValidationError(
                'Данный username использует другую почту.'
            )
        if (
            not CustomUser.objects.filter(username=value).exists()
            and CustomUser.objects.filter(
                email=self.initial_data.get('email')
            ).exists()
        ):
            raise serializers.ValidationError(
                'Данный email использует другой username.'
            )
        return value

    class Meta:
        fields = ("username", "email")
        model = CustomUser


class TokenSerializer(serializers.Serializer):
    """Создадим сериалайзер для получения JWT-токена"""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
