from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import CourseModel, LessonModel
from materials.validators import validate_name_forbidden, VideoLinkValidator


# Для сериализатора для модели курса реализуйте поле вывода уроков.
# Вывод реализуйте с помощью сериализатора для связанной модели.
# Один сериализатор должен выдавать и количество уроков курса
# и информацию по всем урокам курса одновременно.


class LessonSerializer(serializers.ModelSerializer):
    # video_link = serializers.CharField()

    class Meta:
        model = LessonModel
        fields = ("name", "description", "course", "video_link")
        extra_kwargs = {
            "course": {"required": False}
        }  # Сделать поле необязательным для заполнения вообще это лучше убрать, и знать какой id курса
        validators = [VideoLinkValidator(field="video_link")]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курсов"""

    count_lesson_in_course = SerializerMethodField()
    lessons = LessonSerializer(
        many=True, read_only=True, required=False
    )  # вложенный сериализатор не редактируется
    name = serializers.CharField(validators=[validate_name_forbidden])

    def get_count_lesson_in_course(self, course) -> int:
        """Функция нового поля и подсчета количества уроков в конкретном курсе
        по полю course(fk) в уроках и id самих курсов и поля lessons"""
        return LessonModel.objects.filter(course=course.pk).count()

    # def get_lessons(self, course):
    #     # Здесь ты можешь определить, как будут выбираться уроки для курса
    #     lessons = LessonModel.objects.filter(course=course.pk)
    #     return LessonSerializer(lessons, read_only=True, many=True).data

    class Meta:
        model = CourseModel
        fields = "__all__"

    def create(self, validated_data):
        """Функция, создания через сериализатор в представления ViewSet"""
        lessons_data = validated_data.pop(
            "lessons", None
        )  # Удаление поля методом создания при Post запросе
        course = CourseModel.objects.create(
            **validated_data
        )  # Создание курсов и распаковка
        if lessons_data:
            for lesson_data in lessons_data:
                LessonModel.objects.create(course=course, **lesson_data)
        return course


class SubscribeToggleSerializer(serializers.Serializer):
    """
    Сериализатор для валидации входных данных при подписке/отписке от курса.
    """
    course_id = serializers.IntegerField(
        required=True,
        help_text="ID курса, на который пользователь хочет подписаться или отписаться."
    )

    def validate_course_id(self, value):
        """
        Проверяет, существует ли курс с данным ID.
        Если курс не найден, вызывает ValidationError.
        Если найден, возвращает объект CourseModel вместо ID.
        """
        try:
            course = CourseModel.objects.get(id=value)
        except CourseModel.DoesNotExist:
            raise serializers.ValidationError("Курс с указанным ID не найден.")
        return course # Возвращаем сам объект курса, это удобно для дальнейшего использования в View