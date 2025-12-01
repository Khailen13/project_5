from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_video_link


class LessonSerializer(ModelSerializer):
    video_link = CharField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True)
    subscription = SerializerMethodField()

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course.id).count()

    def get_subscription(self, course):
        user = self.context['request'].user
        subscription = Subscription.objects.filter(course=course, user=user).exists()
        return subscription

    class Meta:
        model = Course
        fields = (
            "name",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "subscription",
        )

class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"