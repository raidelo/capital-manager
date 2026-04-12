from decimal import Decimal
from typing import Sequence

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from capital_manager.core.db.models import Account, Transaction
from capital_manager.core.models.transaction import TransactionType


def get_balance(account: Account, db: Session) -> Decimal:
    result = db.execute(
        select(
            func.sum(
                case(
                    (
                        Transaction.type == TransactionType.EXPENSE,
                        Transaction.amount * -1,
                    ),
                    else_=Transaction.amount,
                )
            )
        ).where(Transaction.account_id == account.id)
    ).scalar_one()

    return result


def get_balances(
    accounts: Sequence[Account],
    db: Session,
) -> list[tuple[Account, Decimal]]:
    return [(acc, get_balance(acc, db)) for acc in accounts]
