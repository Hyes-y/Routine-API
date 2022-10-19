from django.conf import settings
from rest_framework.permissions import BasePermission, SAFE_METHODS
import jwt


class IsOwnerOrReadOnly(BasePermission):
    """
    작성자 외 읽기 권한만 부여
    JWT 토큰을 decode, obj의 user와 해당 user가 일치하는지 확인
    """
    message = "[Access Denied] 게시글 수정, 삭제 권한이 없습니다."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            token = request.headers.get('Authorization').split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT["ALGORITHM"])
            token_user = payload.get('user_id')

            return bool(obj.account_id == token_user)
