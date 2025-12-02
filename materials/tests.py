from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import LessonModel, CourseModel
from users.models import CustomUser


class CourseTestCase(APITestCase):
    """Класс для тестирования представления курсов"""

    def setUp(self):
        """В setUp мы прописывам некие фикстуры можно сказать
        создать какие-то значения. Это для того, что перед каждым выполнением теста
        будет очищаться база и запускаться setUp, который будет создавть то что нам надо
        """

        self.user = CustomUser.objects.create(email="admin@sky.pro")
        self.course = CourseModel.objects.create(
            name="Первый курс", description="Описание первого курса", owner=self.user
        )
        self.lessons = LessonModel.objects.create(
            name="Урок 1", description="Описание урока 1", course=self.course
        )

        self.client.force_authenticate(
            user=self.user
        )  # для того чтобы авторизовать пользователя

    def test_course_retrieve(self):
        """Тест просмотра курса"""
        url = reverse(
            "materials:courses-detail", args=(self.course.pk,)
        )  # courses - это basename в маршруте приложения
        response = self.client.get(
            url
        )  # выбираем гет запрос, так как это детальный просмотр объекта
        data = response.json()
        # print(data) # будет меняться при изменении количества тестов, где создаются новые объекты. Меняется id владельца(owner) и id курса, не знаю должно ли так быть
        # {'id': 1, 'count_lesson_in_course': 1, 'lessons': [{'name': 'Урок 1', 'description': 'Описание урока 1', 'course': 1, 'video_link': None}], 'name': 'Первый курс', 'photo': None, 'description': 'Описание первого курса', 'owner': 1}

        # тестирование статуса выполнение(200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # тестирование проверки значения в поле
        self.assertEqual(
            data.get("name"), self.course.name  # либо просто строку "Первый курс"
        )

        # тестируем то, что приходит в json ответе
        # self.assertEqual(
        #     response.json(),
        #
        #     {'id': 1, 'count_lesson_in_course': 1,
        #      'lessons': [{'name': 'Урок 1', 'description': 'Описание урока 1', 'course': 1, 'video_link': None}],
        #      'name': 'Первый курс', 'photo': None, 'description': 'Описание первого курса', 'owner': 1}
        # ) # ВАЖНО ТЕСТЫ ЗАПУСКАТЬ ПО ОТДЕЛЬНОСТИ, ИНАЧЕ МЕНЯЮТСЯ ID тк пополняется БД возможно причина в другом

    def test_course_create(self):
        """Тест создания курса"""
        url = reverse(
            "materials:courses-list"
        )  # courses - это basename в маршруте приложения
        data = {"name": "Какой-то курс"}

        response = self.client.post(
            url, data
        )  # Указываем пост запрос, так как это отправка данных
        # print(response.json()) # {'name': ['Использовано запрещенное слово']} если name задать крипта

        # тестирование статуса выполнение(200)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # тестирование проверка кол-ва объектов в БД
        # Количества два, так как мы еще создали объект в setUp
        self.assertEqual(CourseModel.objects.all().count(), 2)

    def test_course_update(self):
        """Тест обновления курса"""

        data = {"name": "Курс скайпро"}
        url = reverse(
            "materials:courses-detail", args=(self.course.pk,)
        )  # courses - это basename в маршруте приложения
        response = self.client.patch(
            url, data
        )  # выбираем patch запрос, так как это детальный просмотр объекта на обновление

        # тестирование статуса выполнение(200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # тестирование обновилось ли название курса
        self.assertEqual(
            data.get("name"),
            "Курс скайпро",  # название меняется у курса, который создан в setUp
        )

    def test_course_delete(self):
        """Тест удаления курса"""

        url = reverse(
            "materials:courses-detail", args=(self.course.pk,)
        )  # courses - это basename в маршруте приложения
        response = self.client.delete(
            url
        )  # выбираем patch запрос, так как это детальный просмотр объекта на обновление

        # тестирование статуса удаления(204)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # тест на кол-во курсво в бд (0)
        self.assertEqual(CourseModel.objects.all().count(), 0)

    def test_course_list(self):
        """Тестировани списка собак с учетом пагинации"""

        url = reverse("materials:courses-list")
        response = self.client.get(url)
        data_response = response.json()
        # print(data_response)

        data_result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "count_lesson_in_course": 1,
                    "lessons": [
                        {
                            "name": self.lessons.name,
                            "description": self.lessons.description,
                            "course": self.course.pk,
                            "video_link": None,
                        },
                    ],
                    "name": self.course.name,
                    "photo": None,
                    "description": self.course.description,
                    "owner": self.user.pk,
                },
            ],
        }

        # тестирование статуса выполнение(200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # тестирование списка курсов с уроками и пагинацией
        self.assertEqual(data_result, data_response)


class LessonTestCase(APITestCase):
    """Класс для тестирования представления уроков"""

    def setUp(self):
        """В setUp мы прописывам некие фикстуры можно сказать
        создать какие-то значения. Это для того, что перед каждым выполнением теста
        будет очищаться база и запускаться setUp, который будет создавть то что нам надо
        """

        self.user = CustomUser.objects.create(email="admin@sky.pro")
        self.course = CourseModel.objects.create(
            name="Первый курс в тесте уроков",
            description="Описание первого курса в тесте уроков",
            owner=self.user,
        )
        self.lessons = LessonModel.objects.create(
            name="Урок 1 в тесте уроков",
            description="Описание урока 1 в тесте уроков",
            course=self.course,
            owner=self.user,
            video_link="https://www.youtube.com/",
        )  # без owner не работает, это означает, что наставник неверно проверил ДЗ
        # принт -----{'detail': 'You do not have permission to perform this action.'}

        self.client.force_authenticate(
            user=self.user
        )  # для того чтобы авторизовать пользователя

    def test_lesson_retrieve(self):
        """Тест просмотра курса"""
        url = reverse(
            "materials:lesson_retrieve", args=(self.lessons.pk,)
        )  # lesson_retrieve - это namespace в маршруте приложения
        response = self.client.get(
            url
        )  # выбираем гет запрос, так как это детальный просмотр объекта
        data = response.json()
        # print(f"----{data}")
        # тестирование проверки названия урока
        self.assertEqual(data.get("name"), self.lessons.name)

    def test_lesson_create(self):
        """Тест создания уроков"""
        url = reverse("materials:lesson_create")
        data = {
            "name": "Урок 2 для создания уроков",
            "video_link": "https://www.youtube.com/",
            "course": self.course.pk,
        }

        response = self.client.post(
            url, data
        )  # Указываем пост запрос, так как это отправка данных

        # print(response.json())
        # тестирование статуса выполнение(200)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # тестирование проверка кол-ва объектов в БД
        # Количества два, так как мы еще создали объект в setUp
        self.assertEqual(LessonModel.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тест обновления урока"""

        data = {
            "name": "Урок скайпро обновленный",
            # "video_link": "https://www.youtube.com/",
            "course": self.course.pk,
        }
        url = reverse("materials:lesson_update", args=(self.lessons.pk,))
        response = self.client.patch(
            url, data
        )  # выбираем patch запрос, так как это детальный просмотр объекта на обновление
        # print(response.json())
        # тестирование статуса выполнение(200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # тестирование обновилось ли название урока
        self.assertEqual(
            data.get("name"),
            "Урок скайпро обновленный",  # название меняется у курса, который создан в setUp
        )

    def test_lesson_delete(self):
        """Тест удаления урока"""

        url = reverse("materials:lesson_delete", args=(self.lessons.pk,))
        response = self.client.delete(url)
        # тестирование статуса удаления(204)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # тест на кол-во курсво в бд (0)
        self.assertEqual(LessonModel.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тестировани списка уроков с учетом пагинации"""

        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data_response = response.json()
        # print(data_response)

        data_result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "name": self.lessons.name,
                    "description": self.lessons.description,
                    "course": self.course.pk,
                    "video_link": self.lessons.video_link,
                }
            ],
        }

        # тестирование статуса выполнение(200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # тестирование списка курсов с уроками и пагинацией
        self.assertEqual(data_result, data_response)
