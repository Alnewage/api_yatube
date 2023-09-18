from posts.models import Comment, Group, Post
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Post.

    Атрибуты:
        queryset (QuerySet): Запрос для получения всех объектов модели Post.
        serializer_class (Serializer): Сериализатор для модели Post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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

        Исключения:
            PermissionDenied: Если автор объекта не соответствует
            текущему пользователю.
        """
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        """
        Выполняет операцию удаления объекта.

        Аргументы:
            instance (Model): Экземпляр модели Post.

        Исключения:
            PermissionDenied: Если автор объекта не соответствует
            текущему пользователю.
        """
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
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
    """
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        """
        Определяет QuerySet для получения комментариев,
        связанных с определенным постом.
        """
        post_pk = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_pk)

    def perform_create(self, serializer):
        """
        Выполняет операцию создания комментария.

        Аргументы:
            serializer (Serializer): Экземпляр сериализатора.
        """
        serializer.save(author=self.request.user, post_id=int(self.kwargs.get('post_pk')))

    def perform_update(self, serializer):
        """
        Выполняет операцию обновления комментария.

        Аргументы:
            serializer (Serializer): Экземпляр сериализатора.

        Исключения:
            PermissionDenied: Если автор комментария не соответствует
            текущему пользователю.
        """
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save(author=self.request.user, post_id=int(self.kwargs.get('post_pk')))

    def perform_destroy(self, instance):
        """
        Выполняет операцию удаления комментария.

        Аргументы:
            instance (Model): Экземпляр модели Comment.

        Исключения:
            PermissionDenied: Если автор комментария не соответствует
            текущему пользователю.
        """
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()
