from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from capital_manager.core.models.transaction import TransactionType
from capital_manager.core.time import utc_now

from .base import Base


class Account(MappedAsDataclass, Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="account",
        init=False,
    )

    name: Mapped[str] = mapped_column(String(100), unique=True)
    asset: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=utc_now,
    )


class Transaction(MappedAsDataclass, Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)

    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped[Account] = relationship(
        Account,
        back_populates="transactions",
        init=False,
    )

    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=18, scale=6))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=utc_now,
    )
