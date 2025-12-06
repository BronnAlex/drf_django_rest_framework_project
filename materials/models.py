from django.db import models

from users.models import CustomUser


class CourseModel(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    photo = models.ImageField(
        upload_to="materials/photo_courses",
        blank=True,
        null=True,
        verbose_name="Фото курса",
        help_text="Загрузите фото курса",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Добавьте описание курса",
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]


class LessonModel(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    photo_preview = models.ImageField(
        upload_to="materials/photo_lesson",
        blank=True,
        null=True,
        verbose_name="Фото урока",
        help_text="Загрузите фото урока",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Добавьте описание урока",
    )
    course = models.ForeignKey(
        CourseModel,
        on_delete=models.CASCADE,
        verbose_name="Урок из курса",
        help_text="Добавьте к какому курсу относится урок",
        related_name="lessons",
    )
    video_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Добавьте ссылку на видео",
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name"]

# Модель подписки, связывающая пользователя и курс
class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions' # для удобного доступа с user.subscriptions.all()
    )
    course = models.ForeignKey(
        CourseModel,
        on_delete=models.CASCADE,
        related_name='subscribers' #  для удобного доступа с course.subscribers.all()
    )
    date_subscribed = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Гарантирует, что пользователь может подписаться на один курс только один раз
        unique_together = ('user', 'course')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f"{self.user.username} на {self.course.title}"