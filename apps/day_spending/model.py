"""
数据库表模型定义
"""
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from core.model import AbstractBaseModel, TimestampMixin


class TblDaySpending(TimestampMixin, AbstractBaseModel):
    title = fields.CharField(max_length=64, null=False, description="标题")
    spending = fields.FloatField(null=False, description="单笔消费金额")
    describe = fields.CharField(max_length=512, null=True, description="详情")
    spending_date = fields.DateField(null=False, description="消费日期")
    class Meta:
        table = 'tbl_day_spending'
        table_description = '日消费记录表'
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", "is_delete"]


DaySpendingBase = pydantic_model_creator(TblDaySpending, name='DaySpendingBase')
DaySpendingOut = pydantic_model_creator(TblDaySpending, name='DaySpendingOut')
