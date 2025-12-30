from users.models import CustomUser
from celery import shared_task
from django.utils import timezone

from datetime import timedelta
import logging

logger = logging.getLogger(__name__)



@shared_task
def deactivate_inactive_users():
    """
    Деактивирует пользователей, которые не заходили более 30 дней
    """
    try:
        # 30 дней неактивности
        inactive_period_days = 30
        cutoff_date = timezone.now().date() - timedelta(days=inactive_period_days)

        # Находим активных пользователей с последним входом раньше cutoff_date
        # Исключаем суперпользователей и staff
        inactive_users = CustomUser.objects.filter(
            is_active=True,
            last_login__lt=cutoff_date,
            is_superuser=False,
            is_staff=False
        )

        count = inactive_users.count()

        if count > 0:
            # Деактивируем
            inactive_users.update(is_active=False)
            logger.info(f"Деактивировано {count} неактивных пользователей")
            return f"Деактивировано {count} пользователей"
        else:
            logger.info("Нет неактивных пользователей для деактивации")
            return "Нет пользователей для деактивации"

    except Exception as e:
        logger.error(f"Ошибка в задаче deactivate_inactive_users: {e}")
        return f"Ошибка: {e}"