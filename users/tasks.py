from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import CustomUser


@shared_task
def deactivate_user_in_last_login():
    today_30_days_ago = timezone.now().date() - timedelta(days=32)
    last_login = CustomUser.objects.filter(last_login=today_30_days_ago)
    if last_login:
        print(last_login)

    print(last_login)