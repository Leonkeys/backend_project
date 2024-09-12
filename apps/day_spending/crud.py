from typing import List
from .model import TblDaySpending
from core.content import NOT_DELETE, IS_DELETE


async def get_user_list() -> List[TblDaySpending]:
    return await TblDaySpending.filter(is_delete=NOT_DELETE)


async def create_day_spending(day_spending_data) -> TblDaySpending:
    _day_spending = TblDaySpending(**day_spending_data.dict())
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
