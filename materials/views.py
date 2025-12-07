from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample
from drf_yasg.utils import swagger_auto_schema
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
from materials.serializers import CourseSerializer, LessonSerializer, SubscribeToggleSerializer
from users.permissions import IsModeratorPermission, IsOwnerOrPermission


# @method_decorator(name='list', decorator=swagger_auto_schema(
#     operation_description="description from swagger_auto_schema via method_decorator"
# ))
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



# @extend_schema_view(
#     post=extend_schema(
#         summary="Подписка/Отписка от курса",
#         description="Добавляет или удаляет подписку текущего пользователя на указанный курс.",
#         # Явно указываем разрешения для документации.
#         # drf-spectacular ожидает список классов разрешений здесь.
#         # Если IsModeratorPermission | IsOwnerOrPermission не работают напрямую,
#         # вы можете описать их по отдельности или как одно логическое ИЛИ.
#         # Вариант 1: Раздельное описание (для документации)
#         # Если проблема только с DRF Spectaculular
#         # security=[
#         #     {'IsModeratorPermission': []},
#         #     {'IsOwnerOrPermission': []},
#         # ],
#         # Вариант 2: Использование DRF-Spectacular для логических ИЛИ
#         # Это может помочь, если прямая передача OperandHolder вызывает проблему
#         # Если IsModeratorPermission и IsOwnerOrPermission это классы разрешений
#         # то можно сделать так:
#         # security=[
#         #     {'YourAuthScheme': []} # Replace YourAuthScheme with the actual name of your auth scheme defined in settings.py
#         # ],
#         # OR with custom description for permissions
#         parameters=[], # Если есть query params
#         request=SubscribeToggleSerializer, # Указываем сериализатор для входных данных
#         responses={
#             200: OpenApiExample(
#                 'Отписка успешна',
#                 value={"message": "Подписка на курс \"Название курса\" удалена."},
#                 response_only=True,
#                 status_codes=[200]
#             ),
#             201: OpenApiExample(
#                 'Подписка успешна',
#                 value={"message": "Подписка на курс \"Название курса\" добавлена."},
# response_only=True,
#                 status_codes=[201]
#             ),
#             400: OpenApiExample(
#                 'Ошибка валидации',
#                 value={"error": "Параметр 'course_id' обязателен."},
#                 response_only=True,
#                 status_codes=[400]
#             ),
#             404: OpenApiExample(
#                 'Курс не найден',
#                 value={"detail": "Не найдено."}, # Стандартный ответ DRF для 404
#                 response_only=True,
#                 status_codes=[404]
#             ),
#             403: OpenApiExample(
#                 'Нет прав',
#                 value={"detail": "У вас нет разрешения на выполнение этого действия."},
#                 response_only=True,
#                 status_codes=[403]
#             ),
#         }
#     )
# ) # непонятно как использовать drf_spectacular
class SubscribeToggleView(APIView):
    # Указываем, что доступ к этому View разрешен только аутентифицированным пользователям
    permission_classes = (IsModeratorPermission | IsOwnerOrPermission,)

    # def get_permissions(self):
    #     print(f"DEBUG: type(self.permission_classes) = {type(self.permission_classes)}")
    #     print(f"DEBUG: self.permission_classes = {self.permission_classes}")
    #     return super().get_permissions()

    def post(self, request, *args, **kwargs):
        # 1. Инициализируем сериализатор с полученными данными
        # Вся валидация (наличие course_id, его тип, существование курса) будет выполнена сериализатором
        serializer = SubscribeToggleSerializer(data=request.data)

        # 2. Выполняем валидацию. Если данные некорректны, is_valid() вызовет исключение
        # ValidationError и DRF автоматически вернет HTTP 400 Bad Request с деталями ошибок.
        serializer.is_valid(raise_exception=True)

        # 3. Получаем валидированные данные.
        # Поскольку в сериализаторе мы вернули объект CourseModel из validate_course_id,
        # здесь мы сразу получаем объект курса, а не только его ID.
        course_item = serializer.validated_data['course_id']
        user = request.user  # Пользователь из self.request

        # 4. Получаем объекты подписок по текущему пользователю и курсу
        subs_query = Subscription.objects.filter(user=user, course=course_item)

        message = ''
        http_status = status.HTTP_200_OK  # По умолчанию OK

        # 5. Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_query.exists():
            subs_query.delete()
            message = f'Подписка на курс "{course_item.name}" удалена.'
        # 6. Если подписки у пользователя на этот курс нет - создаем ее
        else:
            try:
                Subscription.objects.create(user=user, course=course_item)
                message = f'Подписка на курс "{course_item.name}" добавлена.'
                http_status = status.HTTP_201_CREATED  # 201 Created, так как объект создан
            except Exception as e:
                # В случае уникальных ограничений (unique_together) DRF обычно обрабатывает это лучше,
                # но такой try-except блок остается хорошей практикой для других неожиданных ошибок.
                return Response(
                    {"error": f"Ошибка при добавлении подписки: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # 7. Возвращаем ответ в API
        return Response({"message": message}, status=http_status)