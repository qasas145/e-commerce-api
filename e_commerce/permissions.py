from http import HTTPStatus

class BasePermission :
    def is_admin(self, user_id) :
        pass
    def has_permission_obj(self, user_id, obj_id) :
        print(user_id, obj_id)
        return user_id == obj_id

class IsAuthenticatedOReadOnly(BasePermission) :
    def has_permission_obj(self, user_id, obj_id):
        if not super().has_permission_obj(user_id, obj_id) :
            return ({'detail' : "you don't have permission"}, HTTPStatus.FORBIDDEN)
        return True
    def __repr__(self, user_id, obj_id) -> str:
        return self.has_permission_obj(user_id,  obj_id)
        