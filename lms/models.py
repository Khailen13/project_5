from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название курса")
    preview = models.ImageField(upload_to="lms/course/preview", blank=True, null=True, verbose_name="Превью курса")
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Создатель курса"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата и время последнего обновления")
    price = models.PositiveIntegerField(default=0, verbose_name="Стоимость курса")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return str(f"Курс '{self.name}'")


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")
    preview = models.ImageField(upload_to="lms/lesson/preview", blank=True, null=True, verbose_name="Превью урока")
    video_link = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео урока")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name="Курс", blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Создатель урока"
    )
    price = models.PositiveIntegerField(default=0, verbose_name="Стоимость урока")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return str(f"Урок '{self.name}'")


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Подписчик")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    class Meta:
        verbose_name = "Подписка на обновления курса"
        verbose_name_plural = "Подписки на обновления курса"
