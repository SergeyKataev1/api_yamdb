"""Проект спринта 10: модуль контроллер приложения Api."""
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, CustomUser, Genre, Review, Title

from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorIsAdminIsModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegisterDataSerializer,
                          ReviewSerializer, TitleGetSerializer,
                          TitleSerializer, TokenSerializer, UserEditSerializer,
                          UserSerializer)


class NameSlugBaseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Абстрактный класс-вьюсет, база для классификации свойств предмета."""
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(NameSlugBaseViewSet):
    """Класс-вьюсет для Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(NameSlugBaseViewSet):
    """Класс-вьюсет для Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """Классы-вьюсет для Title."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    # category - фильтрует по полю slug категории
    # genre - фильтрует по полю slug жанра
    # name - фильтрует по названию произведения
    # year - фильтрует по году
    # GET http://127.0.0.1:8000/api/v1/titles/?category=movie&year=1994
    # GET http://127.0.0.1:8000/api/v1/titles/?genre=tale&category=book
    # !!!!! А нужна настройка набора объектов.
    # Что это?????
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    # настройка сортировки
    # GET http://127.0.0.1:8000/api/v1/titles/?ordering=-rating # сортировка по убыванию
    # GET http://127.0.0.1:8000/api/v1/titles/?ordering=-rating # сортировка по возрастанию
    ordering_fields = ['name', 'year', 'rating']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    """Классы-вьюсет для Review."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorIsAdminIsModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(ModelViewSet):
    """Классы-вьюсет для Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorIsAdminIsModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    """Регистрация пользователя с получением пин-кода
    и повторное получение пин-кода"""
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    current_user = CustomUser.objects.filter(username=username)
    email = serializer.validated_data['email']
    current_email = CustomUser.objects.filter(email=email)
    try:
        if current_user.exists() and not current_email.exists():
            raise ValidationError(
                'Данный username использует другой email.'
            )
        if current_email.exists() and not current_user.exists():
            raise ValidationError(
                'Данный email использует другой username.'
            )
        if not CustomUser.objects.filter(
                username=username, email=email
        ).exists():
            # Если пары username и email нет в базе, то сохраняем
            serializer.save()
        # Получаем объект CustomUser с данными пользователя
        user = get_object_or_404(
            CustomUser,
            username=serializer.validated_data['username']
        )
    except IntegrityError:
        raise ValidationError('username или email уже занят')

    # Генерируем код подтверждения
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='YaMDb registration',
        message=f'Your confirmation code: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """Создадим функцию получения JWT-токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        CustomUser,
        username=serializer.validated_data['username']
    )

    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Создадим модель пользователя"""
    lookup_field = 'username'
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

    @action(
        methods=['get', 'patch', ],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == 'GET':
            return Response(
                self.get_serializer(user).data, status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
