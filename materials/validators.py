from rest_framework.serializers import ValidationError

forbidden_words = ["ставки", "гараж", "крипта"]


def validate_name_forbidden(value):

    if value.lower() in forbidden_words:
        raise ValidationError("Использовано запрещенное слово")


class VideoLinkValidator:
    """Валидатор ссылки на видео только ютуб"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):

        # Кортеж с допустимыми префиксами
        youtube_prefixes = (
            "https://www.youtube.com/",
            "http://www.youtube.com/",
            "https://m.youtube.com/",
            "http://m.youtube.com/",
            "https://youtube.com/",  # Не забываем без www
            "http://youtube.com/",  # Не забываем без www
            "https://youtu.be/",  # Сокращенный домен
            "http://youtu.be/",  # Сокращенный домен
        )

        field_value = dict(value).get(self.field)
        if field_value:
            value_lower = field_value.lower()
            validate_value = value_lower.startswith(youtube_prefixes)

            if not validate_value:
                raise ValidationError("Не корректная ссылка Youtube")
