from typing import Annotated

import typer

from capital_manager.cli.db_utils import ensure_db_initialized
from capital_manager.cli.utils import (
    DYELLOW,
    account_list_table,
    build_balances_table,
    get_console,
)
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

        table = account_list_table(accounts)

        console = get_console()
        console.print(table)


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
def account_balance(name: Annotated[str | None, typer.Argument()] = None):
    """Show the current balance of an account"""
    ensure_db_initialized()
    try:
        with SessionMaker() as db:
            if name is None:
                accounts = services.list_accounts(db)
                balances = services.get_balances(accounts, db)

                title = "Account Balances"
            else:
                account = services.get_account_by_name(name, db)
                balance = services.get_balance(account, db)
                balances = [(account, balance)]
                title = f"Balance: [bold {DYELLOW}]{account.name}[/bold {DYELLOW}]"

            table = build_balances_table(balances, title)

            console = get_console()
            console.print(table)

    except ValueError as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)
