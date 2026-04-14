from decimal import Decimal, InvalidOperation
from typing import Annotated

import typer

from capital_manager.cli.db_utils import ensure_db_initialized
from capital_manager.cli.utils import get_console, transaction_list_table
from capital_manager.core import services
from capital_manager.core.db.session import SessionMaker
from capital_manager.core.models.transaction import TransactionCreate, TransactionType

app = typer.Typer(help="Manage transactions")


@app.command("list")
def transaction_list():
    """List all transactions"""
    ensure_db_initialized()
    with SessionMaker() as db:
        txs = services.list_transactions(db)

        if not txs:
            print("No transactions found")
            raise typer.Exit(code=0)

        table = transaction_list_table(txs)

        console = get_console()
        console.print(table)


@app.command("add")
def transaction_add(
    account: Annotated[str, typer.Argument()],
    amount: Annotated[str, typer.Argument()],
    type: Annotated[TransactionType, typer.Argument()],
    description: Annotated[str | None, typer.Option(..., "-d", "--description")] = None,
):
    """Add a transaction"""
    ensure_db_initialized()
    try:
        amount_decimal = Decimal(amount)
    except InvalidOperation:
        print("Error: Invalid amount")
        raise typer.Exit(code=1)

    if amount_decimal <= 0:
        print("Error: Amount must be greater than 0")
        raise typer.Exit(code=1)

    try:
        with SessionMaker() as db:
            tx = services.add_transaction(
                data=TransactionCreate(
                    type=type,
                    amount=amount_decimal,
                    description=description,
                    account_name=account,
                ),
                db=db,
            )
    except ValueError as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)

    print(f"{tx.type.value.capitalize()} of {tx.amount} added to account '{account}'")
