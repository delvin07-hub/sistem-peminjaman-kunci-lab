from rest_framework.permissions import BasePermission


class IsPenanggungJawab(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user and user.is_authenticated
            and hasattr(user, 'penanggung_jawab')
            and user.penanggung_jawab.aktif
        )