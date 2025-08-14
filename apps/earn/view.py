from typing import List
from fastapi import APIRouter
from apps.earn import schema, model, crud
from utils.response_code import ResultResponse


router = APIRouter()

# 日收入
@router.get('/day/listEarn',
            summary='获取单日收入列表',
            description='获取单日收入列表',
            response_model=ResultResponse[List[model.DaySpendingOut]])
async def get_spending_list():
    spend_list = await crud.get_day_spend_list()
    return ResultResponse[List[model.DaySpendingOut]](result=spend_list)


@router.post("/day/createEarn",
             summary="创建单日收入",
             description="创建单日收入",
             response_model=ResultResponse[model.DaySpendingBase]
             )
async def add_day_spending(day_spending: model.DaySpendingOut):
    _day_spending = await crud.create_day_spending(day_spending)
    return ResultResponse[model.DaySpendingOut](result=_day_spending)


@router.put("/day/updateSpend",
            summary="编辑单日收入清单",
            description="编辑单日收入清单",
            response_model=ResultResponse[int])
async def set_day_spending(day_spend: schema.SetDaySpending):
    _day_spending = await crud.update_day_spending(day_spend)
    return ResultResponse[int](result=_day_spending)


@router.delete("/day/deleteSpend",
               summary="删除单日收入清单",
               description="删除单日收入清单",
               response_model=ResultResponse[int])
async def del_day_spending(day_spend_id: int):
    _day_spending = await crud.delete_day_spending(day_spend_id)
    return ResultResponse[int](result=_day_spending)

