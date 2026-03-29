from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from capital_manager.core.db.models import Account, Transaction
from capital_manager.core.models.account import AccountCreate
from capital_manager.core.models.transaction import TransactionCreate
from capital_manager.core.time import utc_now

# -------- ACCOUNTS --------


def create_account(data: AccountCreate, db: Session) -> Account:
    existent = db.execute(
        select(Account).where(Account.name == data.name)
    ).scalar_one_or_none()

    if existent is not None:
        raise ValueError(f'Account "{data.name}" already exists')

    account = Account(
        name=data.name,
        asset=data.asset,
        created_at=utc_now(),
    )

    try:
        db.add(account)
        db.commit()
        db.refresh(account)
        return account
    except Exception:
        db.rollback()
        raise


def get_account_by_name(name: str, db: Session) -> Account:
    account = db.execute(
        select(Account).where(Account.name == name)
    ).scalar_one_or_none()

    if account is None:
        raise ValueError(f'Account "{name}" not found')

    return account


def list_accounts(db: Session) -> Sequence[Account]:
    return db.execute(select(Account)).scalars().all()


# -------- TRANSACTIONS --------


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
