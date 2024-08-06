from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, max_length=35, verbose_name='Почта')
    avatar = models.ImageField(upload_to='media/users/avatars', default='media/users/avatars/default_avatar.jpg',
                               verbose_name='Аватар', **NULLABLE)
    num_phone = models.CharField(unique=True, max_length=35, verbose_name='Телефон', **NULLABLE)
    country = models.CharField(verbose_name='Страна', **NULLABLE)

    verification_code = models.CharField(max_length=100, verbose_name='Код подтверждения', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def image_tag(self):
        if self.avatar:
            return mark_safe(f'<img src="{object.avatar}" style="width: 45px; height:45px;" />' % self.avatar)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    def __str__(self):
        return f"{self.email} "

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payments(models.Model):
    method_variants = (
        ('cash', 'наличные'),
        ('transfer', 'перевод'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Пользователь'),
    date_of_payment = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты'),
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE),
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE),
    payment_sum = models.PositiveIntegerField(verbose_name='Cумма платежа')

    payment_method = models.CharField(max_length=50, choices=method_variants, verbose_name='Способ оплаты')

    session_id = models.CharField(max_length=255, verbose_name='Id сессии', **NULLABLE)
    link = models.URLField(max_length=400, verbose_name='Cсылка на оплату', **NULLABLE)

    def __str__(self):
        return f'Оплата для {self.user}'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
