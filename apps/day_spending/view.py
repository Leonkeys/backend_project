from typing import List
from fastapi import APIRouter, Depends, Request
from . import crud, schema, model
from apps.role import crud as role_crud
from utils.response_code import ResultResponse, HttpStatus
from auth.auth_casbin import Authority, get_casbin

router = APIRouter()


@router.get('/list',
            summary='获取单日消费列表',
            description='获取单日消费列表',
            response_model=ResultResponse[List[model.DaySpendingOut]])
async def get_spending_list():
    user_list = await crud.get_user_list()
    return ResultResponse[List[model.DaySpendingOut]](result=user_list)


@router.post("createDaySpending",
             summary="创建单日消费",
             description="创建单日消费",
             response_model=ResultResponse[model.DaySpendingBase]
             )
async def add_day_spending(day_spending: model.DaySpendingOut):
    _day_spending = await crud.create_day_spending(day_spending)
    return ResultResponse[model.DaySpendingOut](result=_day_spending)


@router.put("/updateDaySpending",
            summary="编辑单日消费清单",
            description="编辑单日消费清单",
            response_model=ResultResponse[int])
async def set_day_spending(day_spend: schema.SetDaySpending):
    _day_spending = await crud.update_day_spending(day_spend)
    return ResultResponse[int](result=_day_spending)


@router.delete("/deleteDaySpending",
               summary="删除单日消费清单",
               description="删除单日消费清单",
               response_model=ResultResponse[int])
async def del_day_spending(day_spend_id: int):
    _day_spending = await crud.delete_day_spending(day_spend_id)
    return ResultResponse[int](result=_day_spending)
