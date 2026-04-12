from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from capital_manager.core import services
from capital_manager.core.db.session import get_db
from capital_manager.core.models.account import (
    Account,
    AccountBalanceResponse,
    AccountCreate,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[Account])
def list_accounts(db: Annotated[Session, Depends(get_db)]) -> list[Account]:
    """List all accounts"""
    return [Account.model_validate(acc) for acc in services.list_accounts(db)]


@router.post("/", response_model=Account, status_code=status.HTTP_201_CREATED)
def create_account(
    account: AccountCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Account:
    """Create a new account"""
    try:
        return Account.model_validate(services.create_account(data=account, db=db))
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))


@router.get(
    "/balance", response_model=AccountBalanceResponse | list[AccountBalanceResponse]
)
def get_account_balance(
    db: Annotated[Session, Depends(get_db)],
    account_id: int | None = None,
    account_name: str | None = None,
) -> AccountBalanceResponse | list[AccountBalanceResponse]:
    """Show the current balance of an account"""
    if account_name == "":
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Must provide a non-empty string for account_name",
        )

    match (account_id, account_name):
        case (None, None):
            accounts = services.list_accounts(db)
            balances = services.get_balances(accounts, db)
            return [
                AccountBalanceResponse(account=Account.model_validate(acc), balance=bal)
                for acc, bal in balances
            ]

        case (account_id, None):
            try:
                account = services.get_account_by_id(account_id, db)
            except ValueError as e:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

        case (None, account_name):
            try:
                account = services.get_account_by_name(account_name, db)
            except ValueError as e:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

        case (account_id, account_name):
            try:
                account_by_id = services.get_account_by_id(account_id, db)
            except ValueError:
                account_by_id = None

            try:
                account_by_name = services.get_account_by_name(account_name, db)
            except ValueError:
                account_by_name = None

            if (
                account_by_id is None
                or account_by_name is None
                or account_by_id.id != account_by_name.id
            ):
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    detail=f'Account with id: {account_id} and name: "{account_name}" not found',
                )

            account = account_by_id

    balance = services.get_balance(account, db)
    return AccountBalanceResponse(
        account=Account.model_validate(account), balance=balance
    )
