from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from capital_manager.core.db.models import Account, Transaction
from capital_manager.core.models.account import AccountCreate
from capital_manager.core.models.transaction import TransactionCreate, TransactionType
from capital_manager.core.services.accounts import create_account
from capital_manager.core.services.transactions import add_transaction

type AccountData = tuple[str, str]
type TransactionData = tuple[TransactionType, str, str, str | None]


def missing_data_details(
    input: Any, locs: list[list[str]]
) -> dict[str, list[dict[str, str | list[str] | Any]]]:
    return {
        "detail": [
            {
                "type": "missing",
                "loc": loc,
                "msg": "Field required",
                "input": input,
            }
            for loc in locs
        ]
    }


def create_accounts(accounts: list[AccountData], db: Session) -> list[Account]:
    ret_accounts = []
    for name, asset in accounts:
        ret_accounts.append(
            create_account(
                AccountCreate.model_validate({"name": name, "asset": asset}),
                db,
            )
        )
    return ret_accounts


def add_transactions(
    transactions: list[TransactionData], db: Session
) -> list[Transaction]:
    ret_transactions = []
    for type, amount, account_name, description in transactions:
        ret_transactions.append(
            add_transaction(
                TransactionCreate.model_validate(
                    {
                        "type": type,
                        "amount": amount,
                        "account_name": account_name,
                        "description": description,
                    }
                ),
                db,
            )
        )

    return ret_transactions


def transactions_to_create(account_name: str) -> list:
    return [
        {
            "type": TransactionType.INCOME,
            "amount": "100.000000",
            "account_name": account_name,
            "description": "TestDescription1",  # with description
        },
        {
            "type": TransactionType.EXPENSE,
            "amount": "50.000000",
            "account_name": account_name,
            # no description — testing optional field
        },
    ]


def calculate_balance_from_transactions(
    account: Account, transactions: list[Transaction]
) -> Decimal:
    return Decimal(
        sum(
            [
                Decimal(tx.amount) * (-1 if tx.type == TransactionType.EXPENSE else 1)
                for tx in transactions
                if tx.account_id == account.id
            ]
        )
    )
