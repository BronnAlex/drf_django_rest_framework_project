from django.core.mail import send_mail
from celery import shared_task
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from materials.models import CourseModel, Subscription


@shared_task
def send_email_for_update_course(course_id):
    """Отправка email подписчикам при обновлении курса"""
    try:
        update_course = CourseModel.objects.get(pk=course_id)

        # Используем flat=True для получения плоского списка
        emails = list(Subscription.objects.filter(course=update_course)
                      .select_related('user')
                      .values_list('user__email', flat=True))

        # Фильтруем пустые email
        emails = [email for email in emails if email]

        if emails:
            send_mail(
                subject=f'Обновлен курс {update_course.name}',
                message='Ознакомьтесь с обновлением курса',
                from_email=EMAIL_HOST_USER,
                recipient_list=emails,
                fail_silently=False,
            )
            print(f"Email отправлен {len(emails)} подписчикам курса '{update_course.name}'")
            print(f'{emails}')
        else:
            print(f"У курса '{update_course.name}' нет подписчиков с email")

    except CourseModel.DoesNotExist:
        print(f"Курс с id={course_id} не найден")
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")


@shared_task
def send_email_birth_day():
    today = timezone.now().today()
    print(today)