from rest_framework import viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from materials.models import CourseModel, LessonModel
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Простой ViewSet-класс представления по реализации CRUD в postman
    """

    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer


class LessonCreateAPIView(CreateAPIView):
    """
    Простой generic.CreateAPIView -класс представления для создания (записи данных в БД)

    """

    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer


class LessonListAPIView(ListAPIView):
    """
    Простой generic.ListAPIView -класс представления вывода всех списков в из БД
    """

    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    Простой generic.RetrieveAPIView -класс представления

    """

    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    """
    Простой generic.UpdateAPIView -класс представления для обновления данных

    """

    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    """
    Простой generic.DestroyAPIView -класс представления для удаления данных

    """

    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
