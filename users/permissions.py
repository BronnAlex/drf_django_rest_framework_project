from rest_framework import permissions


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
