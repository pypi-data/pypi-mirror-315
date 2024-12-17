import strawberry
from strawberry.types import Info

from strawberry_django_jwt.object_types import DeleteType
from strawberry_django_jwt.refresh_token import resolvers
from strawberry_django_jwt.refresh_token.decorators import ensure_refresh_token
from strawberry_django_jwt.refresh_token.object_types import RevokeType


class Revoke:
    @strawberry.mutation
    @ensure_refresh_token
    def revoke(self, info: Info, refresh_token: str) -> RevokeType:
        return resolvers.revoke(info, refresh_token)


class DeleteRefreshTokenCookie:
    @strawberry.mutation
    def delete_cookie(self, info: Info) -> DeleteType:
        return resolvers.delete_cookie(info)
