from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# (email='admin@example11.com')
class CustomUser(AbstractBaseUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Введите почту"
    )
    phone = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name="Телефон",
        help_text="Введите телефон",
    )
    city = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatar",
        null=True,
        blank=True,
        verbose_name="Аватар",
        help_text="Укажите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(AbstractBaseUser):
    CASH = "Наличные"
    NON_CASH = "Безналичные"

    METHODS_PAYMENTS = [
        (CASH, "Наличные"),
        (NON_CASH, "Безналичные"),
    ]
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    paid_course_or_lesson = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Оплата курса или урока",
        help_text="Укажите курс или урок",
    )
    object_id = (
        models.PositiveIntegerField()
    )  # object_id: ID конкретного объекта этой модели. Указал самостоятельно, в усл ДЗ нет такого
    # GenericForeignKey просто удобный интерфейс к связанному объекту, автоматичски найдет id работает по всему проекту,
    # не зависимо от приложений и импортов, при условии, делает поиск по созданию экземпляра класса, делает поиск,
    # на основании какого класса был создан экземпляр, так работает content_type, а id присваивает уже от класса pk

    paid_item = GenericForeignKey("paid_course_or_lesson", "object_id")
    # это поле указывается при создании экземпляра,
    # в котором используется ContentType, а поле  с FK
    # вообще не используется  paid_item=course

    amount_payment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма платежа",
        help_text="Введите сумму платежа",
    )

    date_pay = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата платежа",
        help_text="Укажите дату платежа",
    )

    method_payment = models.CharField(
        max_length=100,
        choices=METHODS_PAYMENTS,
        verbose_name="Способ оплаты",
        help_text="Укажите способ оплаты",
        default=CASH,
    )

    def __str__(self):
        if self.paid_item:
            return f"Платеж за {self.paid_item.__class__.__name__}: '{self.paid_item}' ({self.amount_payment})"
        return 0

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["date_pay", "method_payment", "paid_course_or_lesson"]
