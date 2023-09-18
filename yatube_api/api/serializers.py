from posts.models import Comment, Group, Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.

    Атрибуты:
        author (StringRelatedField): Поле для отображения автора
        по имени пользователя.
    """

    author = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group',)
        read_only_fields = ('author',)


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.
    """

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description',)


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    Атрибуты:
        author (StringRelatedField): Поле для отображения автора
        по имени пользователя.
    """

    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created',)
        read_only_fields = ('author', 'post', 'created',)
