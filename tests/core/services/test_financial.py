from sqlalchemy.orm import Session

from capital_manager.core.db.models import Account, Transaction
from capital_manager.core.services.financial import get_balance, get_balances
from tests.utils import calculate_balance_from_transactions


def test_get_balance(
    accounts: list[Account], transactions: list[Transaction], db: Session
) -> None:
    account = accounts[0]

    balance = calculate_balance_from_transactions(account, transactions)
    assert get_balance(account, db) == balance


def test_get_balances(
    accounts: list[Account], transactions: list[Transaction], db: Session
) -> None:
    balances = [
        (acc, calculate_balance_from_transactions(acc, transactions))
        for acc in accounts
    ]
    assert get_balances(accounts, db) == balances
