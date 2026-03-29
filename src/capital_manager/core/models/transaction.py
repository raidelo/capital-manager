from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from capital_manager.core.time import utc_now


class TransactionType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: TransactionType
    amount: Decimal = Field(gt=0)
    description: str | None = None


class TransactionCreate(TransactionBase):
    account_name: str


class Transaction(TransactionBase):
    id: int
    account_id: int
    created_at: datetime = Field(default_factory=utc_now)
