from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from core.model import AbstractBaseModel, TimestampMixin


class TblRole(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=32, description='角色名')
    nick_name = fields.CharField(max_length=64, description="角色昵称")
    description = fields.CharField(max_length=256, description='角色描述')

    class Meta:
        table = 'tbl_role'
        table_description = '角色表'
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", "is_delete"]


RoleCreate = pydantic_model_creator(TblRole, name='RoleCreate')
RoleOut = pydantic_model_creator(TblRole, name='RoleOut')
