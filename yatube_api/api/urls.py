from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, GroupViewSet, PostViewSet

app_name = 'api'

# Создаем роутер по умолчанию и регистрируем его.
router = DefaultRouter()
router.register(r'posts', PostViewSet,)
router.register(r'groups', GroupViewSet,)

# Здесь мы создаём отдельный роутер для комментариев к постам
# и регистрируем его.
comment_router = DefaultRouter()
comment_router.register(r'comments', CommentViewSet, basename='post-comments',)

urlpatterns = [
    # Маршрут для токенов.
    path('api-token-auth/', views.obtain_auth_token,),

    # Данный роутер будет поддерживать маршруты:
    # /posts/
    # /posts/{post_id}/
    # /groups/
    # /groups/{group_id}/
    path('', include(router.urls),),

    # Этот роутер будет поддерживать маршруты для комментариев к постам:
    # /posts/{post_id}/comments/
    # /posts/{post_id}/comments/{comment_id}/
    path('posts/<int:post_id>/', include(comment_router.urls),),
]
