from typing import List
from fastapi import APIRouter
from apps.spend import schema, model, crud
from utils.response_code import ResultResponse

# 日消费
router = APIRouter()


@router.get('/day/listSpend',
            summary='获取单日消费列表',
            description='获取单日消费列表',
            response_model=ResultResponse[List[model.DaySpendingOut]])
async def get_spending_list():
    spend_list = await crud.get_day_spend_list()
    return ResultResponse[List[model.DaySpendingOut]](result=spend_list)


@router.post("/day/createSpend",
             summary="创建单日消费",
             description="创建单日消费",
             response_model=ResultResponse[model.DaySpendingBase]
             )
async def add_day_spending(day_spending: model.DaySpendingOut):
    _day_spending = await crud.create_day_spending(day_spending)
    return ResultResponse[model.DaySpendingOut](result=_day_spending)


@router.put("/day/updateSpend",
            summary="编辑单日消费清单",
            description="编辑单日消费清单",
            response_model=ResultResponse[int])
async def set_day_spending(day_spend: schema.SetDaySpending):
    _day_spending = await crud.update_day_spending(day_spend)
    return ResultResponse[int](result=_day_spending)


@router.delete("/day/deleteSpend",
               summary="删除单日消费清单",
               description="删除单日消费清单",
               response_model=ResultResponse[int])
async def del_day_spending(day_spend_id: int):
    _day_spending = await crud.delete_day_spending(day_spend_id)
    return ResultResponse[int](result=_day_spending)


# 月固定消费
@router.get('/month/listSpend',
            summary='获取月固定消费列表',
            description='获取月固定消费列表',
            response_model=ResultResponse[List[model.MonthFixedSpendOut]])
async def get_spending_list():
    spend_list = await crud.get_month_fixed_spend_list()
    return ResultResponse[List[model.MonthFixedSpendOut]](result=spend_list)


@router.post("/month/createSpend",
             summary="创建月固定消费",
             description="创建月固定消费",
             response_model=ResultResponse[model.MonthFixedSpendBase]
             )
async def add_day_spending(month_spending: model.MonthFixedSpendOut):
    month_fixed_spend = await crud.create_month_fixed_spend(month_spending)
    return ResultResponse[model.MonthFixedSpendOut](result=month_fixed_spend)


@router.put("/month/updateSpend",
            summary="编辑月固定消费",
            description="编辑月固定消费",
            response_model=ResultResponse[int])
async def set_day_spending(month_fixed_spend: schema.SetMonthFixedSpend):
    month_fixed_spend = await crud.update_month_fixed_spend(month_fixed_spend)
    return ResultResponse[int](result=month_fixed_spend)


@router.delete("/month/deleteSpend",
               summary="删除月固定消费",
               description="删除月固定消费",
               response_model=ResultResponse[int])
async def del_day_spending(month_fixed_spend_id: int):
    month_fixed_spend = await crud.delete_month_fixed_spend(month_fixed_spend_id)
    return ResultResponse[int](result=month_fixed_spend)


# 年固定消费
@router.get('/year/listSpend',
            summary='获取年固定消费列表',
            description='获取年固定消费列表',
            response_model=ResultResponse[List[model.YearFixedSpendOut]])
async def get_spending_list():
    spend_list = await crud.get_year_fixed_spend_list()
    return ResultResponse[List[model.YearFixedSpendOut]](result=spend_list)


@router.post("/year/createSpend",
             summary="创建年固定消费",
             description="创建年固定消费",
             response_model=ResultResponse[model.YearFixedSpendBase]
             )
async def add_day_spending(year_spending: model.YearFixedSpendOut):
    year_fixed_spend = await crud.create_year_fixed_spend(year_spending)
    return ResultResponse[model.YearFixedSpendOut](result=year_fixed_spend)


@router.put("/year/updateSpend",
            summary="编辑年固定消费",
            description="编辑年固定消费",
            response_model=ResultResponse[int])
async def set_day_spending(year_fixed_spend: schema.SetYearFixedSpend):
    year_fixed_spend = await crud.update_year_fixed_spend(year_fixed_spend)
    return ResultResponse[int](result=year_fixed_spend)


@router.delete("/year/deleteSpend",
               summary="删除年固定消费",
               description="删除年固定消费",
               response_model=ResultResponse[int])
async def del_day_spending(year_fixed_spend_id: int):
    year_fixed_spend = await crud.delete_year_fixed_spend(year_fixed_spend_id)
    return ResultResponse[int](result=year_fixed_spend)
