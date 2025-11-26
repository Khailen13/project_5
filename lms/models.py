from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название курса")
    preview = models.ImageField(upload_to="lms/course/preview", blank=True, null=True, verbose_name="Превью курса")
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")
    preview = models.ImageField(upload_to="lms/lesson/preview", blank=True, null=True, verbose_name="Превью урока")
    video_link = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео урока")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name="Курс", blank=True, null=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
