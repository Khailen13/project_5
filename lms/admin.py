from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "creator", "price"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "creator", "price"]
