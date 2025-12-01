from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name="Номер телефона")
    city = models.CharField(max_length=75, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(upload_to="users/avatars", blank=True, null=True, verbose_name="Аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", blank=True, null=True)
    date = models.DateField(verbose_name="Дата оплаты", blank=True, null=True)
    paid_course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="Оплаченный курс", blank=True, null=True
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, verbose_name="Оплаченный урок", blank=True, null=True
    )
    payment_amount = models.FloatField(verbose_name="Сумма оплаты", blank=True, null=True)
    payment_method = models.CharField(max_length=8, choices=PAYMENT_METHOD_CHOICES)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

