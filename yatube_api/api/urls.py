from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from api.views import CommentViewSet, GroupViewSet, PostViewSet

app_name = 'api'

# Создаем роутер по умолчанию и регистрируем его.
router = DefaultRouter()
router.register(r'posts', PostViewSet, )
router.register(r'groups', GroupViewSet, )

# Создаем вложенный роутер для комментариев и регистрируем его.
nested_router = NestedDefaultRouter(router, r'posts', lookup='post', )
nested_router.register(r'comments', CommentViewSet, basename='post-comments', )

urlpatterns = [

    # Маршрут для токенов.
    path('api-token-auth/', views.obtain_auth_token, ),

    # Данный роутер будет поддерживать маршруты:
    # /posts/
    # /posts/{post_id}/
    # /groups/
    # /groups/{group_id}/
    path('', include(router.urls), ),

    # Данный вложенный роутер будет поддерживать следующий маршруты:
    # /posts/{post_id}/comments/
    # /posts/{post_id}/comments/{comment_id}/
    path('', include(nested_router.urls), ),

]
