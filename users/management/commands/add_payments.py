from django.core.management.base import BaseCommand

from lms.models import Lesson, Course
from users.models import User, Payment


class Command(BaseCommand):
    help = "Add products to the database"

    def handle(self, *args, **kwargs):
        # Удаление существующих записей
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()
        Payment.objects.all().delete()

        # Создание курсов
        course_1 = Course.objects.create(name=f"Курс 1")
        course_2 = Course.objects.create(name=f"Курс 2")

        # Создание уроков
        lesson_1 = Lesson.objects.create(name="Урок 1-1", course=course_1)
        lesson_2 = Lesson.objects.create(name="Урок 2-1", course=course_2)
        lesson_3 = Lesson.objects.create(name="Урок 2-2", course=course_2)

        # Создание пользователей
        user_1 = User.objects.create(email="1@mail.ru")
        user_2 = User.objects.create(email="2@mail.ru")
        user_3 = User.objects.create(email="3@mail.ru")

        payments = [
            {"user": user_1, "date": "2021-01-01", "paid_course": course_1, "payment_amount": 100000, "payment_method": "transfer"},
            {"user": user_2, "date": "2022-02-02", "paid_lesson": lesson_2, "payment_amount": 2000, "payment_method": "cash"},
            {"user": user_3, "date": "2023-03-03", "paid_lesson": lesson_3, "payment_amount": 3000, "payment_method": "cash"},

        ]

        for payment in payments:
            Payment.objects.create(**payment)
            self.stdout.write(self.style.SUCCESS(f"Successfully added payment: {payment}"))

