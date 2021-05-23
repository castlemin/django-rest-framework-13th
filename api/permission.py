from rest_framework import permissions


# Authorized 중 User만 수정가능
class IsUserOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Authenticated 되었는 지 확인
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # GET / HEAD / OPTION 에 대하여 True
            return True
            # 그 외 request
        return obj.user == request.user
