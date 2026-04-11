from sqlalchemy.orm import Session

from capital_manager.core.db.models import Account, Transaction
from capital_manager.core.services.financial import get_balance
from tests.utils import calculate_balance_from_transactions


def test_get_balance(
    accounts: list[Account], transactions: list[Transaction], db: Session
) -> None:
    account = accounts[0]

    balance = calculate_balance_from_transactions(account, transactions)
    assert get_balance(account, db) == balance
