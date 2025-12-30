from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

from users.models import CustomUser, Payments, PaymentLinkModel
from users.permissions import IsOwnerOrPermission, IsModeratorPermission, UpdateLastLoginPermission
from users.serializers import PaymentSerializer, UserSerializer, PaymentLinkSerializer
from users.services import  create_stripe_price, create_stripe_session



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
        user.last_login = timezone.now().date()
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
    permission_classes = (IsOwnerOrPermission & UpdateLastLoginPermission, )


class UserDestroyAPIView(DestroyAPIView):
    """
    Простой generic.DestroyAPIView -класс представления для удаления данных

    """

    # Только для авторизованных пользователей
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsModeratorPermission | IsOwnerOrPermission & UpdateLastLoginPermission)





class PaymentLinkModelCreateAPIView(CreateAPIView):
    serializer_class = PaymentLinkSerializer
    queryset = PaymentLinkModel.objects.all()



    def perform_create(self, serializer):
        """Данная функция для того, что мы установили username=None в моделе"""
        payment = serializer.save(
            user=self.request.user
        )  # создался платеж у которого есть сумма, теперь ее надо конвертировать. Надо создать стоимость и сгенерировать ссылку на оплату
        amount_in_rub = payment.amount
        price = create_stripe_price(amount_in_rub)
        session_id, payment_link = create_stripe_session(price)
        # в объект платежа в поле session_id в моделе записываем сессион id, которое получили
        payment.session_id = session_id
        payment.link_payment = payment_link
        payment.save()
