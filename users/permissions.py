from django.utils import timezone
from rest_framework import permissions


class UpdateLastLoginPermission(permissions.BasePermission):
    """Permission для обновления last_login"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            self._update_last_login(request.user)
        return True

    def _update_last_login(self, user):
        try:
            today = timezone.now().date()
            if not user.last_login or user.last_login != today:
                user.last_login = today
                user.save(update_fields=['last_login'])
        except Exception:
            pass


class IsModeratorPermission(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором"""

    message = "Пользователь не является модератором"

    def has_permission(self, request, view):
        """Ф-ция проверки, входит ли пользователь в группу модераторов или нет"""
        return request.user.groups.filter(name="moderators").exists()


class IsOwnerOrPermission(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем"""

    def has_object_permission(self, request, view, obj):

        if obj.owner == request.user:
            return True
        return False
        # # Разрешения на чтение разрешены для любого запроса,
        # # поэтому всегда разрешаем запросы GET, HEAD или OPTIONS.
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        #
        # # Экземпляр должен иметь атрибут с именем `owner`.
        # return obj.owner == request.user
