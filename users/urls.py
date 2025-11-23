from rest_framework.routers import SimpleRouter

from users.views import PaymentsViewSet

app_name = "users"

# Описание маршрутизации для ViewSet
router = SimpleRouter()
router.register("user", PaymentsViewSet)

urlpatterns = []

urlpatterns += router.urls