from typing import List
from .model import TblDaySpending
from core.content import NOT_DELETE, IS_DELETE
from datetime import datetime


async def get_spend_list() -> List[TblDaySpending]:
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
