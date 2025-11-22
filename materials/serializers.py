from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import CourseModel, LessonModel

#Для сериализатора для модели курса реализуйте поле вывода уроков.
# Вывод реализуйте с помощью сериализатора для связанной модели.
# Один сериализатор должен выдавать и количество уроков курса
# и информацию по всем урокам курса одновременно.


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonModel
        fields = ('name', 'description')


class CourseSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели курсов """
    count_lesson_in_course = SerializerMethodField()
    lessons = LessonSerializer(many=True)


    def get_count_lesson_in_course(self, course):
        """ Функция нового поля и подсчета количества уроков в конкретном курсе
        по полю course(fk) в уроках и id самих курсов и поля lessons """
        return LessonModel.objects.filter(course=course.pk).count()
    class Meta:
        model = CourseModel
        fields = ('name', 'description', 'count_lesson_in_course', 'lessons')


    def create(self, validated_data):
        """ Функция, создания через сериализатор в представления ViewSet """
        lessons_data = validated_data.pop('lessons') # Удаление поля методом создания при Post запросе
        course = CourseModel.objects.create(**validated_data) # Создание курсов и распаковка
        for lesson_data in lessons_data:
            LessonModel.objects.create(course=course, **lesson_data)
        return course
