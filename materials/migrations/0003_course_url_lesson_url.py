# Generated by Django 5.0.7 on 2024-08-03 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_alter_course_preview_alter_lesson_preview_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='url',
            field=models.URLField(blank=True, max_length=150, null=True, verbose_name='Ссылка'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='url',
            field=models.URLField(blank=True, max_length=150, null=True, verbose_name='Ссылка'),
        ),
    ]
