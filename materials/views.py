from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

# from rest_framework.permissions import AllowAny
from materials.models import CourseModel, LessonModel, Subscription
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
                ~IsModeratorPermission & IsOwnerOrPermission,
            )  # уже условие получше, не модератор и владелец
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
    permission_classes = (~IsModeratorPermission & IsOwnerOrPermission,)


class SubscribeToggleView(APIView):
    # Указываем, что доступ к этому View разрешен только аутентифицированным пользователям
    permission_classes = (IsModeratorPermission | IsOwnerOrPermission,)

    def post(self, request, *args, **kwargs):
        # 1. Получаем пользователя из self.request
        # request.user автоматически предоставляется DRF после аутентификации
        user = request.user

        # 2. Получаем ID курса из self.request.data (POST-данные)
        # Используем .get() для безопасного доступа, чтобы избежать KeyError
        course_id = request.data.get('course_id')

        # Проверяем, был ли передан course_id
        if not course_id:
            return Response(
                {"error": "Параметр 'course_id' обязателен."},
                status=status.HTTP_400_BAD_REQUEST # 400 Bad Request
            )

        # 3. Получаем объект курса из базы с помощью get_object_or_404
        # Если курс с таким ID не найден, будет автоматически возвращен HTTP 404
        course_item = get_object_or_404(CourseModel, id=course_id)

        # 4. Получаем объекты подписок по текущему пользователю и курсу
        # Используем .filter(), так как .get() вызовет исключение, если объекта нет
        # или если их несколько (хотя unique_together предотвращает последнее)
        subs_query = Subscription.objects.filter(user=user, course=course_item)

        message = ''
        http_status = status.HTTP_200_OK # По умолчанию OK

        # 5. Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_query.exists():
            # Удаляем все найденные подписки (в идеале, будет только одна)
            subs_query.delete()
            message = f'Подписка на курс "{course_item.name}" удалена.'
        # 6. Если подписки у пользователя на этот курс нет - создаем ее
        else:
            try:
                # Создаем новую подписку
                Subscription.objects.create(user=user, course=course_item)
                message = f'Подписка на курс "{course_item.name}" добавлена.'
                http_status = status.HTTP_201_CREATED # 201 Created, так как объект создан
            except Exception as e:
                # Обработка возможной ошибки при создании (например, если unique_together не сработал бы,
                # но в нашем случае он должен предотвращать дубликаты)
                return Response(
                    {"error": f"Ошибка при добавлении подписки: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # 7. Возвращаем ответ в API
        return Response({"message": message}, status=http_status)