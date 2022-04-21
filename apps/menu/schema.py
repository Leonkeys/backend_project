from pydantic import Field

from .model import MenuBase
from typing import List


class MenuCreate(MenuBase):
    pass

    class Config:
        """
        请求参数例子
        """
        schema_extra = {
            "example": {
                "title": "首页",
                "name": "root",
                "path": "/",
                "method": "GET",
                "meta": '{"a":1}'
            }
        }


class MenuTree(MenuBase):
    id: int = Field(..., description="权限id")
    children: List = Field(default=None, description="权限子树")
    hidden: bool = Field(default=True, description="是否隐藏功能")


class MenuList(MenuBase):
    id: int = Field(..., description="权限id")
    children: List = Field(default=None, description="权限子树")


class CurrentMenu(MenuBase):
    id: int = Field(..., description="权限id")
    children: List = Field(default=None, description="权限子树")
    show: bool = Field(default=False, description="是否拥有权限")


class SetMenu(MenuBase):
    id: int = Field(..., description="权限id")

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "title": "机器人管理",
                "name": "robotList",
                "path": "/robot/list",
                "method": "GET",
                "parent_id": 1
            }
        }
