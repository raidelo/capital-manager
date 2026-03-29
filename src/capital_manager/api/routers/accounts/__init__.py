from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from capital_manager.core import services
from capital_manager.core.db.session import get_db
from capital_manager.core.models.account import Account, AccountCreate

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
