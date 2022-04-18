"""
数据库表模型定义
"""
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from core.model import AbstractBaseModel, TimestampMixin


class TblUser(TimestampMixin, AbstractBaseModel):
    username = fields.CharField(max_length=64, unique=True)
    nickname = fields.CharField(max_length=128, null=True)
    is_super = fields.SmallIntField(default=0)
    mobile = fields.CharField(max_length=15, null=True)
    email = fields.CharField(max_length=64, unique=True, null=True)
    password = fields.CharField(max_length=128, null=False)
    avatar = fields.CharField(max_length=256, null=True)

    class Meta:
        table = "tbl_user"
        table_description = "用户表信息"
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", 'is_delete']


UserBase = pydantic_model_creator(TblUser, name="UserBase")
UserOut = pydantic_model_creator(
    TblUser,
    name='UserOut',
    include=['username', 'nickname', 'mobile', 'email'])
