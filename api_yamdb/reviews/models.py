"""Проект спринта 10: модуль управления моделями приложения reviews."""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from .validators import model_validate_username, model_validate_year


class CustomUser(AbstractUser):
    """Модель пользователя."""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    CHOICES_ROLE = [
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
    ]
    username = models.CharField(
        max_length=settings.MAX_LENGTH_USERNAME,
        verbose_name='Имя пользователя',
        help_text='Ваше имя на сайте',
        unique=True,
        validators=[model_validate_username],
    )
    email = models.EmailField(
        max_length=settings.MAX_LENGTH_EMAIL,
        verbose_name='Электронная почта',
        unique=True,
    )
    role = models.CharField(
        verbose_name='статус',
        max_length=max(len(role) for role, _ in CHOICES_ROLE),
        choices=CHOICES_ROLE,
        default=USER,
    )
    bio = models.TextField(
        verbose_name='О себе',
        help_text='Введите информацию про себя',
        blank=True,
    )
    first_name = models.CharField(max_length=150,
                                  verbose_name='Имя',
                                  help_text='Укажите имя пользователя',
                                  blank=True,
                                  )
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия',
                                 help_text='Укажите фамилию пользователя',
                                 blank=True,
                                 )
    CONCLUSION_STR = (
        'Пользователь: {username:.20}, '
        'Имя: {first_name:.20}, '
        'Фамилия: {last_name:.20}, '
        'email: {email}, '
        'Статус: {role}, '
        'О пользователе: {bio:.20}, '
        'pk: {pk}'
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.CONCLUSION_STR.format(
            bio=self.bio,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            role=self.role,
            pk=self.pk
        )


class NameSlugBaseModel(models.Model):
    """Родительский класс для Genre и Category"""

    name = models.CharField(max_length=settings.MAX_LENGTH_NAME,
                            verbose_name='название',
                            help_text="Введите название",
                            blank=False
                            )
    slug = models.SlugField(max_length=settings.MAX_LENGTH_SLUG, unique=True,
                            verbose_name='идентификатор',
                            help_text='Введите идентификатор',
                            blank=False
                            )

    CONCLUSION_STR = (
        f'{name}, имеет идентификатор: {slug}'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.CONCLUSION_STR.format(
            name=self.name,
            slug=self.slug,
        )


class Category(NameSlugBaseModel):
    """Класс управления данными категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugBaseModel):
    """Класс управления данными жанров."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Класс управления данными произведений."""
    name = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        verbose_name='Названием',
        help_text='Укажите название произведения',
        # unique=True,
        blank=False,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        help_text='Укажите год выпуска',
        validators=[model_validate_year],
        blank=False
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Опишите произведение',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        help_text='Выберите категорию, к которой относится произведение'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='жанр',
        blank=False
    )

    CONCLUSION_STR = (
        'Произведение: {name:.20}, '
        'Год публикации: {year}, '
        'Категория: {category}, '
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            UniqueConstraint(
                fields=['name', 'year'], name='unique_name_year_title'
            )]

    def __str__(self):
        return self.CONCLUSION_STR.format(
            name=self.name,
            year=self.year,
            category=self.category,
            pk=self.pk
        )


class GenreTitle(models.Model):
    """Класс управления данными жанров произведений."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    CONCLUSION_STR = (
        'У произведения: {title}, жанр: {genre}'
    )

    def __str__(self):
        return self.CONCLUSION_STR.format(
            genre=self.genre,
            title=self.title,
        )


class AuthorTextPubdateBaseModel(models.Model):
    """Базовый класс для Review и Comment"""

    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        blank=False
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст',
        blank=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    CONCLUSION_STR = (
        'Автор: {author}, '
        'Текст: {text:.20}, '
        'Дата: {pub_date}, '
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.CONCLUSION_STR.format(
            author=self.author,
            text=self.text,
            pube_date=self.pub_date,
        )


class Review(AuthorTextPubdateBaseModel):
    """Класс управления данными отзывов к произведениям."""

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение для отзыва',
        on_delete=models.CASCADE,
        blank=False
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        help_text='Оцените произведение',
        blank=False,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    CONCLUSION_STR = (
        'Произведение: {title}, '
        'Автор отзыва: {author}, '
        'Отзыв: {text:.20}, '
        'Оценка: {score}, '
        'Дата отзыва: {pub_date}, '
    )

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_title',
            )
        ]
        ordering = ('-pub_date',)

    def __str__(self):
        return self.CONCLUSION_STR.format(
            author=self.author,
            title=self.title,
            text=self.text,
            scope=self.score,
            pube_date=self.pub_date,
        )


class Comment(AuthorTextPubdateBaseModel):
    """Класс управления данными комментариев к отзывам."""

    review = models.ForeignKey(
        Review,
        verbose_name='Комментируемый отзыв',
        on_delete=models.CASCADE,
        blank=False
    )

    CONCLUSION_STR = (
        'Автор комментария: {author}, '
        'Комментируемый отзыв: {review}'
        'Комментарий: {text:.20}, '
        'Дата комментария: {pub_date}, '
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.CONCLUSION_STR.format(
            author=self.author,
            rewiew=self.review,
            text=self.text,
            pube_date=self.pub_date,
        )
