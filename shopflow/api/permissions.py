from rest_framework import permissions

class IsCartOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.cart.user == request.user
    
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user