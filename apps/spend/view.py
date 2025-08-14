from typing import List
from fastapi import APIRouter
from apps.spend import schema, model, crud
from utils.response_code import ResultResponse
# 日消费
router = APIRouter()


@router.get('/day/list',
            summary='获取单日消费列表',
            description='获取单日消费列表',
            response_model=ResultResponse[List[model.DaySpendingOut]])
async def get_spending_list():
    spend_list = await crud.get_spend_list()
    return ResultResponse[List[model.DaySpendingOut]](result=spend_list)


@router.post("/day/createDaySpending",
             summary="创建单日消费",
             description="创建单日消费",
             response_model=ResultResponse[model.DaySpendingBase]
             )
async def add_day_spending(day_spending: model.DaySpendingOut):
    _day_spending = await crud.create_day_spending(day_spending)
    return ResultResponse[model.DaySpendingOut](result=_day_spending)


@router.put("/day/updateDaySpending",
            summary="编辑单日消费清单",
            description="编辑单日消费清单",
            response_model=ResultResponse[int])
async def set_day_spending(day_spend: schema.SetDaySpending):
    _day_spending = await crud.update_day_spending(day_spend)
    return ResultResponse[int](result=_day_spending)


@router.delete("/day/deleteDaySpending",
               summary="删除单日消费清单",
               description="删除单日消费清单",
               response_model=ResultResponse[int])
async def del_day_spending(day_spend_id: int):
    _day_spending = await crud.delete_day_spending(day_spend_id)
    return ResultResponse[int](result=_day_spending)


# 月固定消费
# todo 月固定消费列表
# todo 添加月固定消费
# todo 编辑月固定消费
# todo 删除月固定消费
# 房租，房贷、车贷等每月固定开支。
# 月度消费报表


# 年固定消费
# todo 年固定消费列表
# todo 添加年固定消费
# todo 删除年固定消费
# 车险 寿险 物业费等一年交一次费的开支
# 年度消费报表

# 指定日期范围消费报表

