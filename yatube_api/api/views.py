from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsOwnerOrReadOnly
from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Post.

    Атрибуты:
        queryset (QuerySet): Запрос для получения всех объектов модели Post.
        serializer_class (Serializer): Сериализатор для модели Post.
        permission_classes (tuple): Кортеж классов разрешений для управления
        доступом к представлению.
            По умолчанию используется (IsAuthenticated, IsOwnerOrReadOnly),
            что означает, что пользователь должен быть аутентифицирован
            и являться владельцем объекта, чтобы иметь доступ к
            небезопасным методам.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        """
        Выполняет операцию создания объекта.

        Аргументы:
            serializer (Serializer): Экземпляр сериализатора.

        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Выполняет операцию обновления объекта.

        Аргументы:
            serializer (Serializer): Экземпляр сериализатора.

        """
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        """
        Выполняет операцию удаления объекта.

        Аргументы:
            instance (Model): Экземпляр модели Post.
        """
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для модели Group.

    Атрибуты:
        queryset (QuerySet): Запрос для получения всех объектов модели Group.
        serializer_class (Serializer): Сериализатор для модели Group.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Comment.

    Атрибуты:
        serializer_class (Serializer): Сериализатор для модели Comment.
        lookup_url_kwarg (str): Имя URL-параметра для поиска комментариев.
        permission_classes (tuple): Кортеж классов разрешений для управления
        доступом к представлению.
            По умолчанию используется (IsAuthenticated, IsOwnerOrReadOnly),
            что означает, что пользователь должен быть аутентифицирован
            и являться владельцем объекта, чтобы иметь доступ к
            небезопасным методам.

    """
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        """
        Определяет QuerySet для получения комментариев,
        связанных с определенным постом.
        """
        self.post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return self.post.comments.all()

    def perform_create(self, serializer):
        """
        Выполняет операцию создания комментария.

        Аргументы:
            serializer (Serializer): Экземпляр сериализатора.
        """
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user,
                        post=post, )

    def perform_update(self, serializer):
        """
        Выполняет операцию обновления комментария.

        Аргументы:
            serializer (Serializer): Экземпляр сериализатора.

        """
        serializer.save(author=self.request.user,
                        post=self.post, )

    def perform_destroy(self, instance):
        """
        Выполняет операцию удаления комментария.

        Аргументы:
            instance (Model): Экземпляр модели Comment.

        """

        instance.delete()
