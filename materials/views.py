from rest_framework import viewsets
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

# from rest_framework.permissions import AllowAny
from materials.models import CourseModel, LessonModel
from materials.paginations import CustomSetPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModeratorPermission, IsOwnerOrPermission


class CourseViewSet(viewsets.ModelViewSet):
    """
    Простой ViewSet-класс представления по реализации CRUD в postman
    """

    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomSetPagination

    def perform_create(self, serializer):
        # автоматическое создание владельца при создании курса
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """Переопределение прав доступа"""
        # создавать могут все авторизованные пользователи и не модераторы
        if self.action in [
            "create",
        ]:
            # Пользователь должен быть не модератором
            self.permission_classes = (~IsModeratorPermission,)
        elif self.action in [
            "update",
            "retrieve",
        ]:
            # Обновлять и просматривать может или модератор или владелец
            self.permission_classes = (IsModeratorPermission | IsOwnerOrPermission,)
        elif self.action == "destroy":
            # удалять может немодератор, но владелец
            self.permission_classes = (
                ~IsModeratorPermission | IsOwnerOrPermission,
            )  # странное условие не модератор или владелец
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """
    Простой generic.CreateAPIView -класс представления для создания (записи данных в БД)

    """

    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModeratorPermission,)

    def perform_create(self, serializer):
        # автоматическое создание владельца при создании Урока
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    """
    Простой generic.ListAPIView -класс представления вывода всех списков в из БД
    """

    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomSetPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    Простой generic.RetrieveAPIView -класс представления

    """

    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModeratorPermission | IsOwnerOrPermission,)


class LessonUpdateAPIView(UpdateAPIView):
    """
    Простой generic.UpdateAPIView -класс представления для обновления данных

    """

    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModeratorPermission | IsOwnerOrPermission,)


class LessonDestroyAPIView(DestroyAPIView):
    """
    Простой generic.DestroyAPIView -класс представления для удаления данных

    """

    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModeratorPermission | IsOwnerOrPermission,)
