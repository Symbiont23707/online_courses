from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from apps.users.models import User


@database_sync_to_async
def get_user(user_uuid):
    try:
        return User.objects.get(uuid=user_uuid)
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode("utf-8")
        query_params = {}
        if '=' in query_string:
            key, value = query_string.split('=')
            query_params[key] = value
        token = query_params.get("token", None)
        token = AccessToken(token)
        user_uuid = token['user_id']
        scope['user'] = await get_user(user_uuid)

        return await self.app(scope, receive, send)
