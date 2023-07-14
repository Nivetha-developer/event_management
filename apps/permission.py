from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.role =='Admin':
                return True
            return False
        except:
            return False
        
class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.role =='Customer':
                return True
            return False
        except:
            return False
        
class IsAppuser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user!="AnonymousUser":
                return True
            return False
        except:
            return False