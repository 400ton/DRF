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

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_payment = models.PositiveSmallIntegerField(verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок', blank=True, null=True)
    payment_amount = models.PositiveBigIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=80, choices=method_variants, default='transfer',
                                      verbose_name='способ оплаты')

    def __str__(self):
        return f'Оплата для {self.user}'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ('-date_payment',)
