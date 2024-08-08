from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from celery import shared_task

from materials.models import Subscription


@shared_task
def send_email_task(course_id):
    """
    Send email to user
    """
    subs = Subscription.objects.filter(course=course_id)
    for sub in subs:
        course = sub.course
        user = sub.user
        send_mail('Обновление', 'Ваша подписка на курсе обновилась'.format(course.title),
                  EMAIL_HOST_USER, [user.email])
        print(f'Письмо отправлено пользователю {user.email}')
