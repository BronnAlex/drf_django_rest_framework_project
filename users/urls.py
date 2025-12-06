from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import (
    PaymentsViewSet,
    UserCreateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = "users"

# Описание маршрутизации для ViewSet
router = SimpleRouter()
router.register("user", PaymentsViewSet)

urlpatterns = [
    path("users_list/", UserListAPIView.as_view(), name="users_list"),
    path("user/<int:pk>/retrieve", UserRetrieveAPIView.as_view(), name="user_retrieve"),
    path("user/<int:pk>/update", UserUpdateAPIView.as_view(), name="user_update"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("user/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user_delete"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]

urlpatterns += router.urls
