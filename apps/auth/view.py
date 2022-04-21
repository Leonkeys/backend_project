# -*- coding: utf-8 -*-
from auth.auth_casbin import get_casbin
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from . import schema
from apps.user import crud as user_crud
from apps.user import model as user_model
from apps.user import schema as user_schema
from core import settings, TOKEN_CLIENT
from utils.response_code import ResultResponse
from utils import logger
from utils.utils import verify_password
from auth.auth import create_access_token, generate_token

router = APIRouter()


@router.post("/login",
             summary="用户登录认证",
             response_model=schema.Token
             )
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    通过用户名和密码登录获取 token 值
    :param form_data:
    :return:
    """
    # 验证用户
    user = await user_crud.get_user_by_name(username=form_data.username)
    if not user:
        logger.info(
            f"用户名认证错误: username:{form_data.username} password:{form_data.password}"
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='username or password error')

    # 验证密码
    if not verify_password(form_data.password, user.password):
        logger.info(
            f"用户密码错误: username:{form_data.username} password:{form_data.password}"
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='username or password error')

    # 登录成功后返回token
    identifier: str = await generate_token()
    TOKEN_CLIENT.set(user.username, identifier, ex=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.username,
                                       identifier=identifier,
                                       expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/register',
             summary='用户注册',
             description='注册新用户',
             response_model=ResultResponse[user_model.UserOut])
async def register(user: schema.UserCreate):
    user = await user_crud.create_user(user)
    return ResultResponse[user_model.UserOut](result=user)


@router.post('/test',
             summary='权限测试接口',
             description='权限测试接口',
             response_model=ResultResponse[bool]
             )
async def test_auth(test: user_schema.UserPerm):
    e = await get_casbin()
    result = await e.has_permission(test.user, test.model, test.act)
    return ResultResponse[bool](result=result)
