from rest_framework import permissions


class CRUDCustomerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return bool(request.user and request.user.is_authenticated)
