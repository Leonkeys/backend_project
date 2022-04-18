from typing import List
from .model import TblMenu


async def get_root_menu() -> List[TblMenu]:
    return await TblMenu.filter(**{"parent_id": None})


async def get_menu_list() -> List[TblMenu]:
    return await TblMenu.all()


async def get_menu_by_parent_id(parent_id) -> List[TblMenu]:
    menu_s = await TblMenu.filter(**{"parent_id": parent_id})
    return menu_s


async def create_menu(menu_data) -> TblMenu:
    _menu = TblMenu(**menu_data.dict())
    await _menu.save()
    return _menu


async def update_menu(menu_data) -> int:
    update_data = menu_data.dict()
    update_data.pop("id")
    return await TblMenu.filter(id=menu_data.id).update(**update_data)


async def delete_menu(menu_id):
    return await TblMenu.filter(id=menu_id).delete()
