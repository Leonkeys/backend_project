from pydantic import Field

from .model import DaySpendingBase
from typing import List


class SetDaySpending(DaySpendingBase):
    id: int = Field(..., description="id")

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "title": "",
                "spending": "",
                "describe": "",
                "spending_date": ""
            }
        }
