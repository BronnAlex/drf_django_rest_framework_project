from rest_framework.pagination import PageNumberPagination


class CustomSetPagination(PageNumberPagination):
    """Кастомная пагинация, устанавливается в представлении списков"""

    page_size = 5  # количество объектов на странице
    page_size_query_param = "page_size"
    max_page_size = 10  # маакс количество объектов на странице
