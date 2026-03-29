from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from capital_manager.core.time import utc_now


class AccountBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    asset: str


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    created_at: datetime = Field(default_factory=utc_now)
