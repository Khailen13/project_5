from rest_framework import serializers


class CourseOrLessonValidator:
    """Проверяет передачу в запросе id одного курса или урока"""

    def __call__(self, attrs):
        paid_course = attrs.get("paid_course")
        paid_lesson = attrs.get("paid_lesson")

        if paid_course and paid_lesson:
            raise serializers.ValidationError("Операция по оплате предусмотрена только для одного курса или урока")

        if not paid_course and not paid_lesson:
            raise serializers.ValidationError(
                'Для оплаты укажите id курса ("paid_course": id) или урока ("paid_lesson": id).'
            )
