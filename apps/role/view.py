from . import crud, schema, model
from fastapi import APIRouter, Request, Depends
from auth.auth_casbin import get_casbin, Authority
from .crud import get_role_by_name
from utils.response_code import HttpStatus, ResultResponse
from typing import List

router = APIRouter()


@router.post("/list",
             summary="角色列表",
             name="角色列表",
             response_model=ResultResponse[List[schema.RoleList]])
async def get_role():
    role_list: List[model.TblRole] = await crud.get_role_list()
    return ResultResponse[List[schema.RoleList]](result=role_list)


@router.get("/detail",
            summary="角色详情",
            name="角色详情",
            response_model=ResultResponse[model.RoleOut])
async def role_detail(role_id: int):
    role = await crud.get_role_by_id(role_id)
    return ResultResponse[model.RoleOut](result=role)


@router.post('/add/role',
             summary='添加角色',
             name='添加角色',
             response_model=ResultResponse[model.RoleCreate],
             dependencies=[Depends(Authority('role,add'))])
async def add_role(role: model.RoleOut):
    if await crud.has_role(role.name):
        return ResultResponse[str](code=HttpStatus.HTTP_601_ROLE_EXIST, message='角色已存在')
    role = await crud.create_role(role)
    return ResultResponse[model.RoleOut](result=role)


@router.put("/set/role",
            summary='编辑角色',
            name='编辑角色',
            response_model=ResultResponse[int]
            )
async def set_role(role: schema.SetRole):
    _role = await crud.update_role(role)
    return ResultResponse[int](result=_role)


@router.delete('/del/role',
               summary='删除角色',
               name='删除角色',
               response_model=ResultResponse[str],
               dependencies=[Depends(Authority('role,del'))])
async def del_role(request: Request, role_name: str):
    result = await crud.delete_role_by_name(role_name)
    if not result:
        return ResultResponse[str](code=HttpStatus.HTTP_600_ROLE_NOT_EXIST, message='角色不存在')
    return ResultResponse[str](message='角色已删除')


@router.post("/setPermission",
             summary="添加角色权限",
             description="添加角色权限",
             response_model=ResultResponse[str],
             dependencies=[Depends(Authority('auth,add'))])
async def set_permission_by_role(perm_info: List[schema.RolePerm]):
    role = await get_role_by_name(perm_info[0].role)
    if not role:
        return ResultResponse[str](code=HttpStatus.HTTP_422_ROLE_NOT_EXIST,
                                   message='角色不存在')
    e = await get_casbin()
    for perm in perm_info:
        res = await e.add_permission_for_role(perm.role, perm.model, perm.act)
        # if res:
        #     return ResultResponse[str](message='添加角色权限成功')
        # else:
        #     return ResultResponse[str](message='添加角色权限失败，权限已存在')

# @router.delete('/del/perm',
#                summary='删除角色权限',
#                description='删除角色权限',
#                dependencies=[Depends(Authority('auth,del'))])
# async def del_role_perm(perm_info: schema.RolePerm):
#     e = await get_casbin()
#     res = await e.remove_permission_for_role(perm_info.role, perm_info.model, perm_info.act)
#     if res:
#         return ResultResponse[str](message='删除角色权限成功')
#     return ResultResponse[str](message='角色权限不存在')
