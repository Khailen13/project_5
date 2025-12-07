from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from users.models import User


@shared_task
def send_course_update_message(course_name, recipient_list: list):
    """Отправляет письмо об обновлении курса"""
    print("send_course_update_message")
    try:
        send_mail(
            "Обновление курса",
            f"Уважаемый подписчик, сообщаем об обновлении курса {course_name}.",
            settings.EMAIL_HOST_USER,
            recipient_list,
        )
    except Exception as e:
        print(f"Ошибка при отправке письма: {str(e)}")

@shared_task
def disable_inactive_users():
    """Блокирует пользователя при неактивности более месяца"""

    time_month_ago = timezone.now() - relativedelta(month=1)
    users = User.objects.filter(is_active=True).exclude(is_superuser=True)
    for user in users:
        if not user.last_login:
            user.is_active = False
        elif user.last_login < time_month_ago:
            user.is_active = False
        user.save()
