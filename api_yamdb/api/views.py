"""Проект спринта 10: модуль контроллер приложения Api."""
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, CustomUser, Genre, Review, Title

from .filters import TitleFilter
from .permissions import (AdminPermission, CategoryAndGenrePermission, IsAdmin,
                          StrongPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer,
                          ReviewSerializer, TitleGetSerializer, RegisterDataSerializer,
                          TitleSerializer, TokenSerializer, UserEditSerializer,
                          UserSerializer)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    """Класс-вьюсет для Category."""
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = (CategoryAndGenrePermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class GenreViewSet(CreateListDestroyViewSet):
    """Класс-вьюсет для Genre."""
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = (CategoryAndGenrePermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class TitleViewSet(ModelViewSet):
    """Классы-вьюсет для Title."""
    queryset = Title.objects.all()
    permission_classes = (AdminPermission,
                          permissions.IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    """Классы-вьюсет для Review."""
    serializer_class = ReviewSerializer
    permission_classes = (StrongPermission,
                          permissions.IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        new_queryset = title.reviews.all()
        return new_queryset

    def create(self, request, *args, **kwargs):
        if Review.objects.filter(
            title=kwargs.get("title_id"),
            author=request.user
        ).exists():
            return Response(
                f"Пользователь {request.user.username} уже оставил отзыв к "
                f"произведению {kwargs.get('title_id')}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, args, kwargs)


class CommentViewSet(ModelViewSet):
    """Классы-вьюсет для Comment."""
    serializer_class = CommentSerializer
    permission_classes = (StrongPermission,
                          permissions.IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        new_queryset = review.comments.all()
        return new_queryset


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    """Создадим функцию для регистрации пользователей"""
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        # Проверяем, есть ли такой пользователь в базе данных
        CustomUser.objects.get(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"]
        )
        # Не было исключения - значит есть
    except ObjectDoesNotExist:
        # Сработало исключение - значит нет, сохраняем в базу
        serializer.save()
    # Получаем объект CustomUser с данными пользователя
    user = get_object_or_404(
        CustomUser,
        username=serializer.validated_data["username"]
    )
    # Генерируем код подтверждения
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="YaMDb registration",
        message=f"Your confirmation code: {confirmation_code}",
        from_email=None,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """Создадим функцию получения JWT-токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        CustomUser,
        username=serializer.validated_data["username"]
    )

    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Создадим модель пользователя"""
    lookup_field = "username"
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', )
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

    @action(
        methods=["get", "patch", ],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
