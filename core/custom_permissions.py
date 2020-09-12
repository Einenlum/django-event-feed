from rest_framework.permissions import BasePermission

EVENT_PERMISSION_EDIT_OWN_EVENT = "edit_own_event"
EVENT_PERMISSION_DELETE_OWN_EVENT = "delete_own_event"


class EventObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH"]:
            return request.user.has_perm(EVENT_PERMISSION_EDIT_OWN_EVENT, obj)

        if request.method == "DELETE":
            return request.user.has_perm(EVENT_PERMISSION_DELETE_OWN_EVENT, obj)

        return True
