#  Разработка LMS-системы
# Описание
Создал джанго проект config и два приложения users и materials
Создал модели и сериализаторы, посторил маршруты и представления CRUD операций 
с помощью generics и viewset из djangorestframework
Доработал сериализатор для модели курсов, добавив количество уроков в курсе 
и полную оснастку вывода уроков данного курса
## Установка
Необходимл склонировать гит репозиторий 
git clone git@github.com:BronnAlex/drf_django_rest_framework_project.git
Также установить все необходимые зависимости 
pip install -r requirements
Использовать постман, Django ORM или загрузить данные из фикстур
python manage.py loaddata fixtures_from_models.json
## Использование
Используется в онлайн сервисах
## Лицензия
Проект распространяется под [лицензией MIT](LICENSE)