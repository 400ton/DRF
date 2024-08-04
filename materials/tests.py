from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from materials.models import Course, Lesson, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test2@test.ru')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test", description="Основы Test")
        self.lesson = Lesson.objects.create(course=self.course, title="Test Lesson", description="Test",
                                            owner=self.user, url="https://www.youtube.com/watch", )

    def test_create_lesson(self):
        """
            Тестирование создание уроков
        """
        url = reverse("materials:lesson_create")
        data = {
            "title": "Test Lesson",
            "description": "Test",
            "course": self.lesson.course.id,
            "url": "https://www.youtube.com/watch",
        }

        response = self.client.post(url, data=data)
        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(data.get("title"), "Test Lesson")
        self.assertEqual(data.get("course"), self.lesson.course.id)
        self.assertEqual(data.get("url"), "https://www.youtube.com/watch")
        self.assertEqual(data.get("description"), "Test")

    def test_getting_lesson_list(self):
        """
            Тестирование получения списка уроков
        """

        url = reverse("materials:lesson_list")

        response = self.client.get(url)
        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)

    def test_lesson_retrieve(self):
        """
            Тестирование получения одного урока
        """
        url = reverse('materials:lesson_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_update_lesson(self):
        """
            Тестирование получения списка уроков
        """
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "title": "Test Lesson",
            "description": "Test1",
            "course": self.lesson.course.id,
            "url": "https://www.youtube.com/watch1",
        }

        response = self.client.put(url, data=data)
        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)
        self.assertEqual(data.get("description"), "Test1")
        self.assertEqual(data.get("url"), "https://www.youtube.com/watch1")
        self.assertEqual(data.get("course"), self.lesson.course.id)


def test_delete_lesson(self):
    """
        Тестирование удаления уроков
    """

    url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
    data = {
        "title": "Test Lesson",
        "description": "Test",
        "course": self.lesson.course.id,
        "url": "https://www.youtube.com/watch",
    }

    response = self.client.delete(url, data=data)
    data = response.json()
    print(data)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test777@localhost')
        self.course = Course.objects.create(title='Програмное обеспечение')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('materials:subscription_create')

    def test_subscription_activate(self):
        """Тест подписки на курс"""
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        response = self.client.post(self.url, data=data)
        data_res = response.json()
        print(data_res)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "message": "Подписка добавлена",
            },
        )
        self.assertTrue(
            Subscription.objects.all().exists(),
        )

    def test_sub_deactivate(self):
        """Тест отписки с курса"""
        Subscription.objects.create(user=self.user, course=self.course)
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        response = self.client.post(self.url, data=data)
        data_res = response.json()
        print(data_res)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.json(),
            {
                "message": "Подписка удалена",
            },
        )
        self.assertFalse(
            Subscription.objects.all().exists(),
        )
