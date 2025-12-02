import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from lms.models import Course


def validate_video_link(value):
    """Проверяет, является ли строка ссылкой на youtube.com"""

    pattern = re.compile(r"^https?://(www.)?youtube\.comp.*")
    if not re.match(pattern, value.lower()):
        raise ValidationError("Ссылка на видео не соответствует адресу YouTube")


class CourseIDExistsValidator:
    """Проверяет наличие Курса со входящим id"""

    def __call__(self, value):
        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError("Курса с таким id в базе данных нет.")
