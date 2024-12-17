from strawberry.types import Info

from strawberry_django_jwt.object_types import DeleteType
from strawberry_django_jwt.refresh_token.object_types import RevokeType
from strawberry_django_jwt.refresh_token.shortcuts import get_refresh_token
from strawberry_django_jwt.settings import jwt_settings


def revoke(info: Info, refresh_token: str) -> RevokeType:
    context = info.context
    refresh_token_obj = get_refresh_token(refresh_token, context)
    refresh_token_obj.revoke(context)
    return RevokeType(revoked=refresh_token_obj.revoked)


def delete_cookie(info: Info) -> DeleteType:
    context = info.context
    refresh_token = context.request.COOKIES.get(
        jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME, None
    )
    context.delete_refresh_token_cookie = bool(refresh_token) and getattr(
        context.request, "jwt_cookie", False
    )
    if context.delete_refresh_token_cookie:
        refresh_token_obj = get_refresh_token(refresh_token, context)
        refresh_token_obj.revoke(context)
        context.response.delete_cookie(jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME)
        return DeleteType(deleted=True)
    return DeleteType(deleted=False)
