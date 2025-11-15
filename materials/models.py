from django.db import models


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
    )
    video_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Добавьте ссылку на видео",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name"]
