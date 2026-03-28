from capital_manager.core.models.account import Account, AccountCreate
from capital_manager.core.models.transaction import Transaction, TransactionCreate
from capital_manager.core.time import utc_now

accounts: list[Account] = []
transactions: list[Transaction] = []

last_account_id = 1
last_tx_id = 1


# -------- ACCOUNTS --------


def create_account(data: AccountCreate) -> Account:
    if any(acc.name == data.name for acc in accounts):
        raise ValueError(f'Account "{data.name}" already exists')

    global last_account_id
    account = Account(
        name=data.name,
        asset=data.asset,
        id=last_account_id,
        created_at=utc_now(),
    )
    last_account_id += 1

    accounts.append(account)
    return account


def get_account_by_name(name: str) -> Account:
    for acc in accounts:
        if acc.name == name:
            return acc

    raise ValueError(f'Account "{name}" not found')


def list_accounts() -> list[Account]:
    return list(accounts)


# -------- TRANSACTIONS --------


def add_transaction(data: TransactionCreate) -> Transaction:
    account = get_account_by_name(data.account_name)

    if data.amount <= 0:
        raise ValueError("Amount must be greater than 0")

    global last_tx_id
    transaction = Transaction(
        type=data.type,
        amount=data.amount,
        description=data.description,
        id=last_tx_id,
        account_id=account.id,
        created_at=utc_now(),
    )
    last_tx_id += 1

    transactions.append(transaction)
    return transaction


def list_transactions() -> list[Transaction]:
    return list(transactions)
