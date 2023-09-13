from rest_framework import permissions


class IsMeOrReadOnly(permissions.BasePermission):
    message = "다른 이용자의 프로필은 수정할 수 없습니다."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.account == request.user


class IsMeOnly(permissions.BasePermission):
    message = "접근 권한이 없습니다."

    def has_object_permission(self, request, view, obj):
        return obj == request.user
