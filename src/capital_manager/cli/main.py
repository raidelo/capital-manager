from decimal import Decimal, InvalidOperation
from typing import Annotated

import typer
import uvicorn

from capital_manager.core import services
from capital_manager.core.models.account import AccountCreate
from capital_manager.core.models.transaction import TransactionCreate, TransactionType

app = typer.Typer()

account_app = typer.Typer()
transaction_app = typer.Typer()

app.add_typer(account_app, name="account")
app.add_typer(transaction_app, name="transaction")


@app.command()
def api(
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True,
):
    """Run the FastAPI server"""
    uvicorn.run(
        "capital_manager.api.main:app",
        host=host,
        port=port,
        reload=reload,
    )


# -------- ACCOUNT SUBCOMMANDS --------


@account_app.command("list")
def cli_list_accounts():
    """List all accounts"""
    accounts = services.list_accounts()

    if not accounts:
        print("No accounts found")
        raise typer.Exit(code=0)

    for acc in accounts:
        print(f"{acc.name} ({acc.asset})")


@account_app.command("create")
def cli_create_account(
    name: Annotated[str, typer.Argument()],
    asset: Annotated[str, typer.Argument()],
):
    """Create a new account"""
    try:
        account = services.create_account(data=AccountCreate(name=name, asset=asset))
    except ValueError as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)

    print(f"Created account: {account.name} ({account.asset})")


# -------- TRANSACTION SUBCOMMANDS --------


@transaction_app.command("list")
def cli_list_transactions():
    """List all transactions"""
    txs = services.list_transactions()

    if not txs:
        print("No transactions found")
        raise typer.Exit(code=0)

    for tx in txs:
        print(
            f"[{tx.account_id}] {tx.type.upper()} {tx.amount} - {tx.description or ''}"
        )


@transaction_app.command("add")
def cli_add_transaction(
    account: Annotated[str, typer.Argument()],
    amount: Annotated[str, typer.Argument()],
    type: Annotated[TransactionType, typer.Argument()],
    description: Annotated[str | None, typer.Option(..., "-d", "--description")] = None,
):
    """Add a transaction"""
    try:
        amount_decimal = Decimal(amount)
    except InvalidOperation:
        print("Error: Invalid amount")
        raise typer.Exit(code=1)

    if amount_decimal <= 0:
        print("Error: Amount must be greater than 0")
        raise typer.Exit(code=1)

    try:
        tx = services.add_transaction(
            data=TransactionCreate(
                type=type,
                amount=amount_decimal,
                description=description,
                account_name=account,
            )
        )
    except ValueError as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)

    print(f"{tx.type.value.capitalize()} of {tx.amount} added to account '{account}'")


if __name__ == "__main__":
    app()
