"""Проект спринта 10: модуль управления моделями приложения reviews."""
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .validators import validate_username, validate_year


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
        max_length=150,
        verbose_name='Имя пользователя',
        help_text='Ваше имя на сайте',
        unique=True,
        validators=[validate_username],
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True, max_length=253)
    role = models.CharField(
        verbose_name='статус',
        max_length=15,
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
        'Пользователь: {username}, '
        'Имя: {first_name}, '
        'Фамилия: {last_name}, '
        'email: {email}, '
        'Статус: {role}'
        'О пользователе: {bio}, '
        'pk : {pk}'
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'Пользоваетель'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.CONCLUSION_STR.format(
            bio=self.bio[:20],
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            role=self.role,
            pk=self.pk
        )


class Category(models.Model):
    """Класс управления данными категорий."""
    name = models.CharField(max_length=256,
                            verbose_name='Название категории',
                            help_text='Cформулируйте наименование категории',
                            blank=False
                            )
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Идентификатор категории',
                            help_text='Присвойте категории уникальный тег',
                            blank=False
                            )

    CONCLUSION_STR = (
        'У категории: {name}, Идентификатор {slug}'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.CONCLUSION_STR.format(
            name=self.name,
            slug=self.slug,
        )


class Genre(models.Model):
    """Класс управления данными жанров."""
    name = models.CharField(max_length=256,
                            verbose_name='Название жанра',
                            help_text='Cформулируйте наименование жанра',
                            blank=False)
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='Идентификатор жанра',
                            help_text='Присвойте жанру уникальный тег',
                            blank=False)

    CONCLUSION_STR = (
        'У жанра: {name}, Идентификатор {slug}'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.CONCLUSION_STR.format(
            name=self.name,
            slug=self.slug,
        )


class Title(models.Model):
    """Класс управления данными произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Названием',
        help_text='Укажите название произведения',
        unique=True,
        blank=False,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        help_text='Укажите год выпуска',
        validators=[validate_year],
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
        'Произведение: {name}, '
        'Год публикации: {year}, '
        'Категория: {category}, '
    )

    class Meta:
        default_related_name = 'title'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

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


class Review(models.Model):
    """Класс управления данными отзывов к произведениям."""
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=False
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение для отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=False)
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва',
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
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    CONCLUSION_STR = (
        'Произведение: {title}, '
        'Автор отзыва: {author}, '
        'Отзыв: {text}, '
        'Оценка: {score}, '
        'Дата отзыва: {pub_date}, '
    )

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('title', 'author', )

    def __str__(self):
        return self.CONCLUSION_STR.format(
            author=self.author,
            title=self.title,
            text=self.text[:20],
            scope=self.score,
            pube_date=self.pub_date,
        )


class Comment(models.Model):
    """Класс управления данными комментариев к отзывам."""
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
        blank=False
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Комментриуемый отзыв',
        on_delete=models.CASCADE,
        blank=False,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария',
        blank=False,
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)
    CONCLUSION_STR = (
        'Автор комментария: {author}, '
        'Коменируемый отзыв: {rewiew}'
        'Комментарий: {text}, '
        'Дата комментария: {pub_date}, '
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.CONCLUSION_STR.format(
            author=self.author,
            rewiew=self.review,
            text=self.text[:20],
            pube_date=self.pub_date,
        )
