from rest_framework import serializers

from posts.models import Comment, Group, Post


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
        fields = '__all__'
        read_only_fields = ('author',)


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.
    """

    class Meta:
        model = Group
        fields = '__all__'


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
        fields = '__all__'
        read_only_fields = ('author', 'post', 'created',)
