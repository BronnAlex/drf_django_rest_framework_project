#  Разработка LMS-системы
# Описание
Создал джанго проект config и два приложения users и materials
Создал модели и сериализаторы, посторил маршруты и представления CRUD операций 
с помощью generics и viewset из djangorestframework
Снова доработал  сериализатор для модели курсов, добавив количество уроков в курсе 
и полную оснастку вывода уроков данного курса, 
Добавил проверку разрешений на операции CRUD
Удалил и создал заново БД, так как изначально не прописал в главных настройках AUTH_USER_MODEL = "users.CustomUser" 
Добавил модель подписки на курс и удаление подписки 

Создал файл Dockerfile и docker-compose.yml

Добавил в проект celery и celery-beate
Написал тесты 
## Установка
Необходимл склонировать гит репозиторий 
git clone git@github.com:BronnAlex/drf_django_rest_framework_project.git
Также установить все необходимые зависимости 
pip install -r requirements
Использовать постман, Django ORM или загрузить данные из фикстур
python manage.py loaddata fixtures_from_models.json
## Использование
Используется в онлайн сервисах
Чтобы использовать docker-compose выполните команды
docker-compose up -d --build Для запуска всех сервисов, определенных в файле docker-compose.yml, используйте команду:
docker-compose down останавливает все работающие контейнеры и удаляет контейнеры, сети, тома и образы, созданные командой docker-compose up
docker-compose exec service_name name_command - позволяет выполнять команды внутри работающего контейнера
Например  docker-compose exec web bash  - Пример выполнения команды bash внутри контейнера web


 

## Лицензия
Проект распространяется под [лицензией MIT](LICENSE)