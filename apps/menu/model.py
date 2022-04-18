"""
数据库表模型定义
"""
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from core.model import AbstractBaseModel, TimestampMixin


class TblMenu(TimestampMixin, AbstractBaseModel):
    title = fields.CharField(max_length=64, null=False, description="展示标题")
    name = fields.CharField(max_length=64, null=False, description="权限名称")
    path = fields.CharField(max_length=64, null=False, description="权限路由")
    method = fields.CharField(max_length=32, null=False, description="请求方法")
    action = fields.CharField(max_length=32, null=False, description="API权限操作")
    is_menu = fields.BooleanField(default=True, description="是否是菜单栏")
    parent_id = fields.IntField(null=True, description="父级id")
    meta = fields.JSONField(null=True, description="附加属性")

    class Meta:
        table = 'tbl_menu'
        table_description = '菜单表'
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", "is_delete"]


MenuBase = pydantic_model_creator(TblMenu, name='MenuBase')
MenuOut = pydantic_model_creator(TblMenu, name='MenuOut')
