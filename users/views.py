from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from users.models import CustomUser, Payments
from users.serializers import PaymentSerializer, UserSerializer


class PaymentsViewSet(viewsets.ModelViewSet):
    """
    Простой ViewSet-класс представления по реализации CRUD в postman модели Payments
    """

    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["date_pay"]  # фильтрация по дате платежа
    filterset_fields = (
        "date_pay",
        "method_payment",
        "paid_course_or_lesson",
    )  # Набор полей для сортировки
    # http://127.0.0.1:8000/users/user?method_payment=Наличные&ordering=-date_pay
    # Таким образом тестируется сортировка и фильтрация в постмане


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (
        AllowAny,
    )  # это разрешение всем (даже анонимным) пользователям на регистрацию, также в маршрутах пропишем отдельно для логина

    def perform_create(self, serializer):
        """Данная функция для того, что мы установили username=None в моделе"""
        user = serializer.save(
            is_active=True
        )  # убрал из скобок is_active=True тк у нас в моделе нет, это вызывает ошибку. (указывать надо сущ поля модели)
        user.set_password(
            user.password
        )  # для того, чтобы захешировался пароль пользователя
        user.save()


class UserListAPIView(ListAPIView):
    """
    Простой generic.ListAPIView -класс представления вывода всех списков в из БД
    """

    # Только для авторизованных пользователей(эти права прописаны в config.settings)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Простой generic.RetrieveAPIView -класс представления

    """

    # Только для авторизованных пользователей
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """
    Простой generic.UpdateAPIView -класс представления для обновления данных

    """

    # Только для авторизованных пользователей
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDestroyAPIView(DestroyAPIView):
    """
    Простой generic.DestroyAPIView -класс представления для удаления данных

    """

    # Только для авторизованных пользователей
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
