from pydantic import Field

from .model import DaySpendingBase, MonthFixedSpendBase, YearFixedSpendBase


class SetDaySpending(DaySpendingBase):
    id: int = Field(..., description="id")

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "title": "",
                "spending": "",
                "describe": "",
                "spend_year": "",
                "spend_month": "",
                "spend_day": "",
            }
        }


class SetMonthFixedSpend(MonthFixedSpendBase):
    id: int = Field(..., description="id")

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "title": "",
                "spend": "",
                "describe": "",
                "spending_date": ""
            }
        }


class SetYearFixedSpend(YearFixedSpendBase):
    id: int = Field(..., description="id")

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "title": "",
                "spend": "",
                "describe": "",
                "spending_date": ""
            }
        }
