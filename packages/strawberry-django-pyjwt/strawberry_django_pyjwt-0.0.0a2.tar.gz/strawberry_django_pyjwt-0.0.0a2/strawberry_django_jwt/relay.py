import inspect

from django.contrib.auth import get_user_model
import strawberry
from strawberry.types.field import StrawberryField
from strawberry.field_extensions import InputMutationExtension
from strawberry.types import Info

from strawberry_django_jwt.decorators import (
    dispose_extra_kwargs,
    ensure_token,
    token_auth,
)
from strawberry_django_jwt.field_extensions import DynamicInputMutationExtension
import strawberry_django_jwt.mixins as mixins
from strawberry_django_jwt.mutations import JSONWebTokenMutation
from strawberry_django_jwt.object_types import (  # TokenPayloadType,
    DeleteType,
    PayloadType,
    TokenDataType,
    TokenPayloadType,
)
from strawberry_django_jwt.settings import jwt_settings
from strawberry_django_jwt.utils import (
    create_strawberry_argument,
    get_context,
    get_payload,
)


class ObtainJSONWebToken(JSONWebTokenMutation):
    """Obtain JSON Web Token mutation"""

    @strawberry.mutation(extensions=[DynamicInputMutationExtension()])
    @token_auth
    @dispose_extra_kwargs
    def obtain(self, info: Info) -> TokenDataType:
        return TokenDataType(payload=TokenPayloadType())


class ObtainJSONWebTokenAsync(ObtainJSONWebToken):
    """No need for async impl, decorators handle it."""


class Verify:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @ensure_token
    def verify(self, info: Info, token: str) -> PayloadType:
        return PayloadType(payload=get_payload(token, info.context))


class VerifyAsync(Verify):
    """No need for async impl, decorators handle it."""


class Refresh(mixins.RelayRefreshMixin):
    pass


class RefreshAsync(mixins.AsyncRelayRefreshMixin):
    pass


class DeleteJSONWebTokenCookie:
    @strawberry.mutation
    def delete_cookie(self, info: Info) -> DeleteType:
        ctx = get_context(info)
        ctx.delete_jwt_cookie = jwt_settings.JWT_COOKIE_NAME in ctx.COOKIES and getattr(
            ctx, "jwt_cookie", False
        )
        return DeleteType(deleted=ctx.delete_jwt_cookie)


class DeleteJSONWebTokenCookieAsync(DeleteJSONWebTokenCookie):
    """No need for async impl, only for consistency."""
