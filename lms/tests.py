from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(name="Урок 1", creator=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("lms:lesson-create")
        data = {"name": "Урок 2"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("lms:lesson-update", args=(self.lesson.pk,))
        data = {"name": "Урок 3"}
        response = self.client.patch(url, data)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json.get("name"), data.get("name"))

    def test_lesson_delete(self):
        url = reverse("lms:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lesson-list")
        response = self.client.get(url)
        # response_json = response.json()
        # expected_result = {
        #     "count": 1,
        #     "next": None,
        #     "previous": None,
        #     "results": [
        #         {
        #             "id": self.lesson.pk,
        #             "video_link": None,
        #             "name": self.lesson.name,
        #             "description": None,
        #             "preview": None,
        #             "course": None,
        #             "creator": self.user.pk,
        #         },
        #     ],
        # }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response_json, expected_result)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name="Курс 1", creator=self.user)

    def test_course_subscription_switch(self):
        # Предварительная проверка статуса подписку
        url_course = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url_course)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_subscription_status = False
        self.assertEqual(response.json().get("subscription"), expected_subscription_status)

        # Проверка после перехода на подписку
        url_subscription = reverse("lms:course-subscription-switch")
        post_data = {"course_id": self.course.id}
        response = self.client.post(url_subscription, post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "Подписка добавлена")
        response = self.client.get(url_course)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_subscription_status = True
        self.assertEqual(response.json().get("subscription"), expected_subscription_status)
