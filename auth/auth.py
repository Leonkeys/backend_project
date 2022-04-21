import random
import string
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple
from core import Jwt, JWTError, ExpiredSignatureError, TOKEN_CLIENT
from fastapi import Request, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2, get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from starlette.authentication import AuthenticationError
from pydantic import ValidationError

from core import settings
from utils import custom_exc
from apps.user.crud import get_user_by_name


class OAuth2CustomJwt(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            description: Optional[str] = None,
            auto_error: bool = True,
    ):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        for url, op in settings.NO_VERIFY_URL.items():
            if op == 'eq' and url == request.url.path.lower():
                return None
            elif op == 'in' and url in request.url.path.lower():
                return None

        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None

        try:
            if isinstance(param, str):
                param = str.encode(param)
            playload = Jwt.decode(
                param,
                settings.SECRET_KEY, algorithm=settings.ALGORITHM
            )
        except ExpiredSignatureError:
            raise custom_exc.TokenExpired()
        except (JWTError, ValidationError, AttributeError):
            raise custom_exc.TokenAuthError()

        _username: str = playload.get('username')
        username = _username[0:-12]
        identifier = _username[-12:]
        redis_identifier: str = TOKEN_CLIENT.get(username)
        if not redis_identifier or identifier != redis_identifier:
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="用户可能已在别处登录"
                )
        user = await get_user_by_name(username=username)
        if not user:
            raise AuthenticationError("用户不存在，认证失败")

        """在 Request 对象中设置用户对象，这样在其他地方就能通过 request.state.user 获取到当前用户了"""
        request.state.user = user


def create_access_token(
        subject: str,
        identifier: str,
        expires_delta: float = None
) -> str:
    """
    生成token
    :param subject:需要存储到token的数据(注意token里面的数据，属于公开的)
    :param authority_id: 权限id(用于权限管理)
    :param expires_delta:
    :return:
    """
    if expires_delta:
        expire = time.time() + expires_delta
    else:
        expire = time.time() + settings.ACCESS_TOKEN_EXPIRE_MINUTES
    to_encode = {"exp": expire, "username": subject + identifier}
    encoded_jwt = Jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def generate_token() -> str:
    length_of_token = 12
    identifier = ""

    for i in range(length_of_token):
        identifier += random.choice(string.ascii_letters)
    return identifier
