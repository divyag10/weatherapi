from datetime import datetime
from typing import List
from pydantic import BaseModel


class ActivityDataSchema(BaseModel):
    id: int
    temperature: float
    humidity: float
    wind: float
    recommendation: str

    class Config:
        orm_mode = True


class DeleteActivitySchema(BaseModel):
    id: int

    class config:
        orm_mode = True
