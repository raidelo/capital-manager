from typing import Sequence

from rich.box import ROUNDED
from rich.console import Console
from rich.table import Column, Table

from capital_manager.core.db.models import Account, Transaction
from capital_manager.core.models.transaction import TransactionType

DCYAN = "#8be9fd"
DGREEN = "#50fa7b"
DRED = "#ff5555"

TITLE_STYLE = f"{DCYAN} bold"
DATETIME_FORMAT = "%F %T"

_console: Console | None = None


def get_console() -> Console:
    global _console
    if _console is None:
        _console = Console()
    return _console


def account_list_table(seq: Sequence[Account]) -> Table:
    t = Table(
        Column("ID", justify="right"),
        Column("Name"),
        Column("Asset"),
        Column("Created at"),
        box=ROUNDED,
        border_style="bold",
        title="Account List",
        title_style=TITLE_STYLE,
    )

    for acc in seq:
        t.add_row(
            str(acc.id),
            acc.name,
            acc.asset,
            acc.created_at.strftime(DATETIME_FORMAT),
        )

    return t


def transaction_list_table(seq: Sequence[Transaction]) -> Table:
    t = Table(
        Column("ID", justify="right"),
        Column("Account"),
        Column("Amount", justify="right"),
        Column("Description"),
        Column("Created at"),
        box=ROUNDED,
        border_style="bold",
        title="Transaction List",
        title_style=TITLE_STYLE,
    )

    for tx in seq:
        sign = "-" if tx.type == TransactionType.EXPENSE else "+"
        color = DRED if tx.type == TransactionType.EXPENSE else DGREEN

        amount = f"[{color}]{sign}{tx.amount:.2f}[/{color}]"

        t.add_row(
            str(tx.id),
            tx.account.name,
            amount,
            tx.description or "\u2014",
            tx.created_at.strftime(DATETIME_FORMAT),
        )

    return t
