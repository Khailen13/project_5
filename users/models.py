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
    date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="Оплаченный курс", blank=True, null=True
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, verbose_name="Оплаченный урок", blank=True, null=True
    )
    amount = models.PositiveIntegerField(default=0, verbose_name="Сумма оплаты")
    method = models.CharField(max_length=8, choices=PAYMENT_METHOD_CHOICES, default="transfer")
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="id сессии",
    )
    link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user}: {self.date}"
