from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = SerializerMethodField()

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course.id).count()

    def get_lessons(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course.id)]

    class Meta:
        model = Course
        fields = (
            "name",
            "preview",
            "description",
            "lessons_count",
            "lessons",
        )
