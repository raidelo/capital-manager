from datetime import datetime

from pydantic import BaseModel, Field

from capital_manager.core.time import utc_now


class AccountBase(BaseModel):
    name: str
    asset: str


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    created_at: datetime = Field(default_factory=utc_now)
