from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import CourseModel, LessonModel


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курсов """
    count_lesson_in_course = SerializerMethodField()

    def get_count_lesson_in_course(self, course):
        """Функция нового поля и подсчета количества уроков в конкретном курсе
        по полю course(fk) в уроках и id самих курсов"""
        return LessonModel.objects.filter(course=course.pk).count()
    class Meta:
        model = CourseModel
        fields = ('name', 'photo', 'description', 'count_lesson_in_course') # '__all__' обязательно надо указать новое поле,
                                                                            # а не выбирать все


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели уроков """
    class Meta:
        model = LessonModel
        fields = "__all__"
