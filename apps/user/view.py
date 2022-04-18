from typing import List
from fastapi import APIRouter, Depends, Request
from . import crud, schema, model
from apps.role import crud as role_crud
from utils.response_code import ResultResponse, HttpStatus
from auth.auth_casbin import Authority, get_casbin

router = APIRouter()


@router.get('/list',
            summary='获取用户列表',
            description='获取用户列表',
            response_model=ResultResponse[List[model.UserOut]])
async def get_user_list():
    user_list = await crud.get_user_list()
    return ResultResponse[List[model.UserOut]](result=user_list)


@router.get("/info",
            summary="获取当前用户信息",
            name="获取当前用户信息",
            response_model=ResultResponse[model.UserOut])
async def get_user_info(request: Request):
    return ResultResponse[model.UserOut](result=request.state.user)


@router.get("/detail",
            summary="用户详情",
            name="用户详情",
            response_model=ResultResponse[model.UserOut])
async def user_detail(request: Request):
    return ResultResponse[model.UserOut](result=request.state.user)


@router.post("/add",
             summary="创建用户",
             name="创建用户",
             response_model=ResultResponse[str])
async def create_user(user: model.UserBase):
    if user.is_super:
        return ResultResponse[str](code=HttpStatus.HTTP_426_WRONGFUL_REQUEST, result="不可以添加该类用户，请联系管理员。")
    _user = await crud.create_user(user)
    return ResultResponse[str](result="用户创建成功。")


@router.put("/set",
            summary="编辑用户信息",
            name="编辑用户信息",
            response_model=ResultResponse[str])
async def update_user(user: schema.UserSet):
    _user = await crud.update_user(user)
    return ResultResponse[str](result="用户编辑成功")


@router.get('/user/roles',
            summary='获取用户角色列表',
            description='获取用户角色列表',
            response_model=ResultResponse[List])
async def get_role_list(username: str):
    e = await get_casbin()
    result = await e.get_roles_for_user(username)
    return ResultResponse[List](result=result)


@router.post("/add/role",
             summary="添加用户角色",
             description="添加用户角色",
             response_model=ResultResponse[str],
             dependencies=[Depends(Authority('auth,add'))])
async def add_user_role(user_role: schema.UserRole):
    user = await crud.get_user_by_name(user_role.user)
    if not user:
        return ResultResponse[str](code=HttpStatus.HTTP_419_USER_EXCEPT, message='添加权限的用户不存在，请检查用户名')
    role = await role_crud.get_role_by_name(user_role.role)
    if not role:
        return ResultResponse[str](code=HttpStatus.HTTP_422_ROLE_NOT_EXIST, message='角色不存在')
    e = await get_casbin()
    res = await e.add_role_for_user(user_role.user, user_role.role)
    if res:
        return ResultResponse[str](message='添加用户角色成功')
    else:
        return ResultResponse[str](message='添加用户角色失败')


@router.delete('/del/role',
               summary='删除用户角色',
               description='删除用户角色',
               response_model=ResultResponse[str],
               dependencies=[Depends(Authority('auth,del'))]
               )
async def del_user_role(user_role: schema.UserRole):
    user = await crud.get_user_by_name(user_role.user)
    if not user:
        return ResultResponse[str](code=HttpStatus.HTTP_419_USER_EXCEPT,
                                   message='用户不存在，请检查用户名')
    role = await role_crud.get_role_by_name(user_role.role)
    if not role:
        return ResultResponse[str](code=HttpStatus.HTTP_422_ROLE_NOT_EXIST,
                                   message='角色不存在')
    e = await get_casbin()
    res = await e.delete_role_for_user(user_role.user, user_role.role)
    if res:
        return ResultResponse[str](message='删除用户角色成功')
    else:
        return ResultResponse[str](message='删除用户角色失败')

# @router.post("/add/perm",
#              summary="添加用户权限",
#              description="添加用户权限",
#              response_model=ResultResponse[str],
#              dependencies=[Depends(Authority('auth,add'))])
# async def add_user_perm(user_info: schema.UserPerm):
#     user = await crud.get_user_by_name(user_info.user)
#     if not user:
#         return ResultResponse[str](code=HttpStatus.HTTP_419_USER_EXCEPT, message='添加权限的用户不存在，请检查用户名')
#     e = await get_casbin()
#     res = await e.add_permission_for_user(user_info.user, user_info.model,
#                                           user_info.act)
#     if res:
#         return ResultResponse[str](message='添加用户权限添加成功')
#     else:
#         return ResultResponse[str](message='添加用户权限失败，权限已存在')
#
#
# @router.delete("/del/perm",
#                summary="删除用户权限",
#                description='删除用户权限',
#                response_model=ResultResponse[str],
#                dependencies=[Depends(Authority('auth,del'))])
# async def del_user_perm(user_info: schema.UserPerm):
#     e = await get_casbin()
#     res = await e.delete_permission_for_user(user_info.user, user_info.model,
#                                              user_info.act)
#     if res:
#         return ResultResponse[str](message='删除用户权限成功')
#     else:
#         return ResultResponse[str](message='删除用户权限失败')
