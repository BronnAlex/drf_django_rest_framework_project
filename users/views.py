from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from users.models import Payments
from users.serializers import PaymentSerializer


class PaymentsViewSet(viewsets.ModelViewSet):
    """
    Простой ViewSet-класс представления по реализации CRUD в postman модели Payments
    """

    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['date_pay'] # фильтрация по дате платежа
    filterset_fields = ("date_pay", "method_payment", "paid_course_or_lesson")  # Набор полей для сортировки
    # http://127.0.0.1:8000/users/user?method_payment=Наличные&ordering=-date_pay
    # Таким образом тестируется сортировка и фильтрация в постмане