# -*- coding: utf-8 -*-
from typing import List, Union, Any
from tortoise.exceptions import DoesNotExist
from . import schema
from .model import TblUser
from utils.utils import get_password_hash
from core.content import NOT_DELETE


async def get_user_by_name(username: str) -> Union[TblUser, Any]:
    """
    :param username:
    :return:
    """
    try:
        user: TblUser = await TblUser.get(username=username)
    except DoesNotExist as exc:
        return None
    return user


async def create_user(user_data: schema.UserCreate) -> TblUser:
    user = TblUser(**user_data.dict(exclude={'confirm'}))
    user.password = get_password_hash(user_data.password)
    await user.save()
    return user


async def update_user(user_data: schema.UserSet):
    _user = user_data.dict(exclude={"id"})
    res = await TblUser.filter(id=user_data.id).update(**_user)
    return res


async def get_user_list() -> List[TblUser]:
    return await TblUser.filter(is_delete=NOT_DELETE)
