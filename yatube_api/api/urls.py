from django.urls import include, path, re_path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, GroupViewSet, PostViewSet

app_name = 'api'

# Создаем роутер по умолчанию и регистрируем его.
router = DefaultRouter()
router.register(r'posts', PostViewSet, )
router.register(r'groups', GroupViewSet, )
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comments',)

urlpatterns = [
    # Маршрут для токенов.
    path('api-token-auth/', views.obtain_auth_token, ),

    # Данный роутер будет поддерживать маршруты:
    # /posts/
    # /posts/{post_id}/
    # /groups/
    # /groups/{group_id}/
    # /posts/{post_id}/comments/
    # /posts/{post_id}/comments/{comment_id}/
    path('', include(router.urls), ),

]
