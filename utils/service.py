from apps.menu.model import TblMenu
from apps.menu.schema import MenuTree
from apps.menu import crud
from apps.user import crud as user_crud
from typing import List
from auth.auth_casbin import get_casbin


async def get_all_menu_tree(current_user) -> List[MenuTree]:
    root_menu_list: List[TblMenu] = await crud.get_root_menu()
    menu_list: List[MenuTree] = []
    for _menu in root_menu_list:
        menu: MenuTree = await _get_children(_menu, current_user)
        menu_list.append(menu)
    return menu_list


async def _get_children(menu: TblMenu, current_user) -> MenuTree:
    menu_id = menu.id
    children_menu: List[TblMenu] = await crud.get_menu_by_parent_id(parent_id=menu_id)
    if await _check_permission(current_user, menu.name, menu.action):
        menu.hidden = False
    else:
        menu.hidden = True
    if children_menu:
        menu.children = [await _get_children(_menu, current_user) for _menu in children_menu]
    return menu


async def _check_permission(user, model, act) -> bool:
    _user = await user_crud.get_user_by_name(username=user)
    if _user.is_super:
        return True
    e = await get_casbin()
    result = await e.has_permission(user, model, act)
    return result


async def get_menu_tree_by_role(current_user, role_name) -> List[MenuTree]:
    root_menu_list: List[TblMenu] = await crud.get_root_menu()
    menu_list: List[MenuTree] = []
    for _menu in root_menu_list:
        if await _check_permission(current_user,  _menu.name, _menu.action):
            menu: MenuTree = await _get_current_children(_menu, current_user, role_name)
            menu_list.append(menu)
    return menu_list


async def _get_current_children(_menu: TblMenu, current_user, role_name) -> MenuTree:
    _menu_id = _menu.id
    current_children_menu: List[TblMenu] = await crud.get_menu_by_parent_id(parent_id=_menu_id)
    if await _check_permission_by_role(role_name, _menu.name, _menu.action):
        _menu.show = True
    else:
        _menu.show = False
    if current_children_menu:
        _menu.children = [await _get_current_children(_menu, current_user, role_name) for _menu in
                          current_children_menu if await _check_permission(current_user, _menu.name, _menu.action)]
    return _menu


async def _check_permission_by_role(role_name, model, act) -> bool:
    e = await get_casbin()
    result = await e.has_permission(role_name, model, act)
    return result
