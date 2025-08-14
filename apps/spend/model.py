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
    spend_year = fields.CharField(max_length=16, null=False, description="消费年份")
    spend_month = fields.CharField(max_length=32, null=False, description="消费月份")
    spend_day = fields.CharField(max_length=64, null=False, description="消费日")

    class Meta:
        table = 'tbl_day_spend'
        table_description = '日消费记录表'
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", "is_delete"]


DaySpendingBase = pydantic_model_creator(TblDaySpending, name='DaySpendingBase')
DaySpendingOut = pydantic_model_creator(TblDaySpending, name='DaySpendingOut')


class TblMonthFixedSpend(TimestampMixin, AbstractBaseModel):
    title = fields.CharField(max_length=128, null=False, description="开支标题")
    spend = fields.FloatField(null=False, description="金额")
    describe = fields.CharField(max_length=512, null=True, description="详情")
    spend_date = fields.CharField(max_length=16, null=False, description="开始统计日期，每月几号")

    class Meta:
        table = "tbl_month_fixed_spend"
        table_description = '月度固定开支'
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", "is_delete"]


MonthFixedSpendBase = pydantic_model_creator(TblMonthFixedSpend, name='MonthFixedSpendBase')
MonthFixedSpendOut = pydantic_model_creator(TblMonthFixedSpend, name='MonthFixedSpendOut')


class TblYearFixedSpend(TimestampMixin, AbstractBaseModel):
    title = fields.CharField(max_length=128, null=False, description="开支标题")
    spend = fields.FloatField(null=False, description="金额")
    describe = fields.CharField(max_length=512, null=True, description="详情")
    spend_date = fields.CharField(max_length=16, null=False, description="统计日期，每年哪天")

    class Meta:
        table = "tbl_year_fixed_spend"
        table_description = '年度固定开支'
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", "is_delete"]


YearFixedSpendBase = pydantic_model_creator(TblYearFixedSpend, name='YearFixedSpendBase')
YearFixedSpendOut = pydantic_model_creator(TblYearFixedSpend, name='YearFixedSpendOut')
