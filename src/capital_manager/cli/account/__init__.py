from typing import Annotated

import typer

from capital_manager.cli.db_utils import ensure_db_initialized
from capital_manager.core import services
from capital_manager.core.db.session import SessionMaker
from capital_manager.core.models.account import AccountCreate

app = typer.Typer(help="Manage accounts")


@app.command("list")
def account_list():
    """List all accounts"""
    ensure_db_initialized()
    with SessionMaker() as db:
        accounts = services.list_accounts(db)

        if not accounts:
            print("No accounts found")
            raise typer.Exit(code=0)

        for acc in accounts:
            print(f"{acc.name} ({acc.asset})")


@app.command("create")
def account_create(
    name: Annotated[str, typer.Argument()],
    asset: Annotated[str, typer.Argument()],
):
    """Create a new account"""
    ensure_db_initialized()
    try:
        with SessionMaker() as db:
            account = services.create_account(
                data=AccountCreate(name=name, asset=asset), db=db
            )
    except ValueError as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)

    print(f"Created account: {account.name} ({account.asset})")


@app.command("balance")
def account_balance(name: Annotated[str, typer.Argument()]):
    """Show the current balance of an account"""
    ensure_db_initialized()
    try:
        with SessionMaker() as db:
            account = services.get_account_by_name(name, db)
            balance = services.get_balance(account, db)
    except ValueError as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)

    print(f"💰 Balance for '{account.name}': {balance:.2f} {account.asset}")
