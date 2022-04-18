from apps.menu.model import TblMenu
from apps.menu import crud
from typing import List
from auth.auth_casbin import get_casbin


async def get_menu_tree(current_user) -> List[TblMenu]:
    root_menu_list: List[TblMenu] = await crud.get_root_menu()
    menu_list: List[TblMenu] = []
    for _menu in root_menu_list:
        menu: TblMenu = await get_children(_menu, current_user)
        menu_list.append(menu)
    return menu_list


async def get_children(menu: TblMenu, current_user) -> TblMenu:
    menu_id = menu.id
    children_menu: List[TblMenu] = await crud.get_menu_by_parent_id(parent_id=menu_id)
    if await check_permission(current_user, menu.name, menu.action):
        menu.hidden = False
    if children_menu:
        menu.children = [await get_children(_menu, current_user) for _menu in children_menu]
    return menu


async def check_permission(user, model, act) -> bool:
    e = await get_casbin()
    result = await e.has_permission(user, model, act)
    return result
