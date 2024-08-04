from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    preview = models.ImageField(upload_to='media/course/preview', **NULLABLE)
    description = models.TextField(max_length=250, verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')
    url = models.URLField(max_length=150, verbose_name='Ссылка', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(max_length=250, verbose_name='описание')
    video = models.FileField(upload_to='media/lesson/video', **NULLABLE)
    preview = models.ImageField(upload_to='media/lesson/preview', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', related_name='course')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')
    url = models.URLField(max_length=150, verbose_name='Ссылка', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="Курс", )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_user_email(self):
        return self.user.email

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}."

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ('user', 'course')
