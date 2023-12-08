# Hello ISP

import time
from typing import Optional

from asgiref.sync import async_to_sync
from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ValidationError

from accounts.models import User, Token


class AuthenticationAsync:
    async def aauthenticate(self, uid: str) -> Optional[User | str]:
        try:
            token = await Token.objects.aget(uid=uid)
        except (Token.DoesNotExist, ValidationError):
            return None
        return (await User.objects.aget_or_create(email=token.email))[0]


class GetUserAsync:
    async def aget_user(self, email: str) -> Optional[User]:
        try:
            return await User.objects.aget(email=email)
        except User.DoesNotExist:
            return None


class PasswordlessAuthenticationBackend(
    AuthenticationAsync, GetUserAsync, BaseBackend
):
    def authenticate(self, request, uid: str) -> Optional[User]:
        return async_to_sync(self.aauthenticate)(uid)

    def get_user(self, user_id: str) -> Optional[User]:
        return async_to_sync(self.aget_user)(user_id)
