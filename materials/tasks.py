from django.core.mail import send_mail
from celery import shared_task
from django.utils import timezone

from config.settings import EMAIL_HOST_USER


@shared_task
def send_email_task_celery(recipient_email):
    """Проверка(тестовой задачи)"""
    # print("Проверка тестовой задачи в Celery")

    send_mail('Подписка на курс', 'Вы подписались на курс', EMAIL_HOST_USER, [recipient_email])


@shared_task
def send_email_birth_day():
    today = timezone.now().today()
    print(today)