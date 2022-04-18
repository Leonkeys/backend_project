from auth.auth_casbin import get_casbin
from .model import RoleCreate, TblRole
from typing import Union, Any, List
from tortoise.exceptions import DoesNotExist
from core.content import NOT_DELETE


async def get_role_list() -> List[TblRole]:
    return await TblRole.filter(is_delete=NOT_DELETE)


async def create_role(role_data: RoleCreate) -> TblRole:
    role = TblRole(**role_data.dict())
    await role.save()
    return role


async def get_role_by_id(role_id: int) -> Union[TblRole, Any]:
    """
    获取角色信息
    """
    try:
        role: TblRole = await TblRole.get(id=role_id)
    except DoesNotExist as exec:
        return None
    return role


async def get_role_by_name(role_name: str) -> Union[TblRole, Any]:
    """
    获取角色信息
    """
    try:
        role: TblRole = await TblRole.get(name=role_name)
    except DoesNotExist as exec:
        return None
    return role


async def update_role(role) -> int:
    update_data = role.dict()
    update_data.pop("id")
    return await TblRole.filter(id=role.id, is_delete=NOT_DELETE).update(**update_data)


async def delete_role_by_name(role_name: str) -> bool:
    """
    删除角色信息，同时删除 casbin 中角色信息
    """
    role: TblRole = await get_role_by_name(role_name)
    if role:
        role.is_delete = 1
        await role.save()

        # 删除 casbin 的角色权限
        e = await get_casbin()
        e.delete_role(role_name)

        return True
    return False


async def has_role(role_name: str) -> bool:
    """
    判断是否包含角色信息
    """
    role: TblRole = await get_role_by_name(role_name)
    if role and not role.is_delete:
        return True
    return False
