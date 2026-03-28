from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionBase(BaseModel):
    type: TransactionType
    amount: Decimal = Field(gt=0)
    description: str | None = None


class TransactionCreate(TransactionBase):
    account_name: str


class Transaction(TransactionBase):
    id: int
    account_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
