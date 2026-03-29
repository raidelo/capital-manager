from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from capital_manager.core import services
from capital_manager.core.db.session import get_db
from capital_manager.core.models.transaction import Transaction, TransactionCreate

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/", response_model=list[Transaction])
def list_transactions(db: Annotated[Session, Depends(get_db)]) -> list[Transaction]:
    """List all transactions"""
    return [Transaction.model_validate(tx) for tx in services.list_transactions(db)]


@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def add_transaction(
    transaction: TransactionCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Transaction:
    """Add a transaction"""
    try:
        return Transaction.model_validate(
            services.add_transaction(data=transaction, db=db)
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
