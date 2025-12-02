from rest_framework.fields import SerializerMethodField, URLField
from rest_framework.serializers import IntegerField, ModelSerializer, Serializer

from lms.models import Course, Lesson, Subscription
from lms.validators import CourseIDExistsValidator, validate_video_link


class LessonSerializer(ModelSerializer):
    video_link = URLField(validators=[validate_video_link], required=False)

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
        user = self.context["request"].user
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


class SubscriptionSerializer(Serializer):
    course_id = IntegerField(
        validators=[
            CourseIDExistsValidator(),
        ]
    )
