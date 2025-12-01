import re

from rest_framework.exceptions import ValidationError


def validate_video_link(value):
    """Проверяет, является ли строка ссылкой на youtube.com"""

    pattern = re.compile(r"^https?://youtube\.com/.*")
    if not re.match(pattern, value.lower()):
        raise ValidationError("Ссылка на видео не соответствует youtube.com")
