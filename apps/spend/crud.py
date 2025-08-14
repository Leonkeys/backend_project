from typing import List
from .model import TblDaySpending, TblMonthFixedSpend, TblYearFixedSpend
from core.content import NOT_DELETE, IS_DELETE
from datetime import datetime


# 日
async def get_day_spend_list() -> List[TblDaySpending]:
    return await TblDaySpending.filter(is_delete=NOT_DELETE)


async def create_day_spending(day_spending_data) -> TblDaySpending:
    day_spending_dict = day_spending_data.dict()
    current_date = datetime.now()
    current_year = str(current_date.year)
    current_month = current_year + "-" + str(current_date.month)
    current_day = current_month + "-" + str(current_date.day)
    day_spending_dict["spending_year"] = current_year
    day_spending_dict["spending_month"] = current_month
    day_spending_dict["spending_day"] = current_day
    _day_spending = TblDaySpending(**day_spending_dict)
    await _day_spending.save()
    return _day_spending


async def update_day_spending(day_spending_data) -> int:
    update_data = day_spending_data.dict()
    day_spending_id = update_data.pop("id")
    return await TblDaySpending.filter(id=day_spending_id).update(**update_data)


async def delete_day_spending(day_spending_id):
    return await TblDaySpending.filter(id=day_spending_id).update(is_delete=IS_DELETE)


async def real_delete_day_spending(day_spending_id):
    return await TblDaySpending.filter(id=day_spending_id).delete()


# 月
async def get_month_fixed_spend_list() -> List[TblMonthFixedSpend]:
    return await TblMonthFixedSpend.filter(is_delete=NOT_DELETE)


async def create_month_fixed_spend(month_fixed_spend_data) -> TblMonthFixedSpend:
    month_fixed_spend = TblMonthFixedSpend(**month_fixed_spend_data.dict())
    await month_fixed_spend.save()
    return month_fixed_spend


async def update_month_fixed_spend(month_fixed_spend_data) -> int:
    update_data = month_fixed_spend_data.dict()
    month_fixed_spend_id = update_data.pop("id")
    return await TblMonthFixedSpend.filter(id=month_fixed_spend_id).update(**update_data)


# 逻辑删除
async def delete_month_fixed_spend(month_fixed_spend_id) -> int:
    return await TblMonthFixedSpend.filter(id=month_fixed_spend_id).update(is_delete=IS_DELETE)


# 物理删除
async def real_delete_month_fixed_spend(month_fixed_spend_id):
    return await TblMonthFixedSpend.filter(id=month_fixed_spend_id).delete()


# 年
async def get_year_fixed_spend_list() -> List[TblYearFixedSpend]:
    return await TblYearFixedSpend.filter(is_delete=NOT_DELETE)


async def create_year_fixed_spend(year_fixed_spend_data) -> TblYearFixedSpend:
    year_fixed_spend = TblYearFixedSpend(**year_fixed_spend_data.dict())
    await year_fixed_spend.save()
    return year_fixed_spend


async def update_year_fixed_spend(year_fixed_spend_data) -> int:
    update_data = year_fixed_spend_data.dict()
    year_fixed_spend_id = update_data.pop("id")
    return await TblYearFixedSpend.filter(id=year_fixed_spend_id).update(**update_data)


# 逻辑删除
async def delete_year_fixed_spend(year_fixed_spend_id) -> int:
    return await TblYearFixedSpend.filter(id=year_fixed_spend_id).update(is_delete=IS_DELETE)


# 物理删除
async def real_delete_year_fixed_spend(year_fixed_spend_id):
    return await TblYearFixedSpend.filter(id=year_fixed_spend_id).delete()
