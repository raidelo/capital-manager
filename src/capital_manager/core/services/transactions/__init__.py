from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from capital_manager.core.db.models import Transaction
from capital_manager.core.models.transaction import TransactionCreate
from capital_manager.core.services.accounts import get_account_by_name
from capital_manager.core.time import utc_now


def add_transaction(data: TransactionCreate, db: Session) -> Transaction:
    account = get_account_by_name(data.account_name, db)

    if data.amount <= 0:
        raise ValueError("Amount must be greater than 0")

    transaction = Transaction(
        account_id=account.id,
        type=data.type,
        amount=data.amount,
        description=data.description,
        created_at=utc_now(),
    )

    try:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    except Exception:
        db.rollback()
        raise


def list_transactions(db: Session) -> Sequence[Transaction]:
    return db.execute(select(Transaction)).scalars().all()
