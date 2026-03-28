from datetime import datetime, timezone

from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    name: str
    asset: str


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
