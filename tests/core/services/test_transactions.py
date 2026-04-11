from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from capital_manager.core.db.models import Account, Transaction
from capital_manager.core.models.transaction import TransactionCreate
from capital_manager.core.services.transactions import (
    add_transaction,
    list_transactions,
)
from tests.utils import transactions_to_create


def test_add_transaction_ok(accounts: list[Account], db: Session) -> None:
    account = accounts[0]
    transactions = transactions_to_create(account.name)

    for tx in transactions:
        transaction = add_transaction(
            TransactionCreate.model_validate(tx),
            db,
        )

        result = db.execute(
            select(Transaction).where(
                and_(
                    Transaction.id == transaction.id,
                    Transaction.account_id == transaction.account_id,
                    Transaction.amount == transaction.amount,
                    Transaction.type == transaction.type,
                    Transaction.description == transaction.description,
                )
            )
        ).scalar_one_or_none()

        assert result is not None
        assert result == transaction


def test_list_transactions(transactions: list[Transaction], db: Session) -> None:
    result = list_transactions(db)

    assert result == transactions
