from utils.response_code import ResultResponse
from typing import List
from utils import service
from . import crud, model, schema
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/menuTree",
            summary="获取菜单树",
            description="获取菜单树",
            response_model=ResultResponse[List[schema.MenuTree]])
async def menu_tree(request: Request):
    current_user = request.state.user.username
    menu_tree: List[model.TblMenu] = await service.get_menu_tree(current_user)
    return ResultResponse[List[schema.MenuTree]](result=menu_tree)


@router.post('/menuByUser',
             summary="获取指定用户所拥有的权限树",
             name="获取指定用户所拥有的权限树",
             response_model=ResultResponse[str])
async def menu_tree_by_user(request: Request, user_id: int):
    pass


@router.post("/createMenu",
             summary="创建菜单",
             description="创建菜单",
             response_model=ResultResponse[model.MenuBase])
async def add_menu(menu: model.MenuOut):
    _menu = await crud.create_menu(menu)
    return ResultResponse[model.MenuOut](result=_menu)


@router.put("/updateMenu",
            summary="编辑菜单",
            description="编辑菜单",
            response_model=ResultResponse[int])
async def set_menu(menu: schema.SetMenu):
    _menu = await crud.update_menu(menu)
    return ResultResponse[int](result=_menu)


@router.delete("/deleteMenu",
               summary="删除菜单",
               description="删除菜单",
               response_model=ResultResponse[int]
               )
async def del_menu(menu_id: int):
    _menu = await crud.delete_menu(menu_id)
    return ResultResponse[int](result=_menu)
