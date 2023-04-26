from rest_framework import permissions
#we creating the permissinos such that only the owner can access the indiviudal contents

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
