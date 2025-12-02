from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("materials/", include("materials.urls", namespace="materials")),
    path("users/", include("users.urls", namespace="users")),
]
