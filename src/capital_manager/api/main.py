from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from capital_manager.core import services
from capital_manager.core.db.models import Base
from capital_manager.core.db.session import engine, get_db
from capital_manager.core.models.account import Account, AccountCreate
from capital_manager.core.models.transaction import Transaction, TransactionCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CapitalManager API")


@app.get("/ping")
def ping():
    """Check API is working"""
    return {"message": "pong"}


# -------- ACCOUNT ENDPOINTS --------


@app.get("/accounts", response_model=list[Account])
def list_accounts(db: Annotated[Session, Depends(get_db)]) -> list[Account]:
    """List all accounts"""
    return [Account.model_validate(acc) for acc in services.list_accounts(db)]


@app.post("/accounts", response_model=Account, status_code=status.HTTP_201_CREATED)
def create_account(
    account: AccountCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Account:
    """Create a new account"""
    try:
        return Account.model_validate(services.create_account(data=account, db=db))
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))


# -------- TRANSACTION ENDPOINTS --------


@app.get("/transactions", response_model=list[Transaction])
def list_transactions(db: Annotated[Session, Depends(get_db)]) -> list[Transaction]:
    """List all transactions"""
    return [Transaction.model_validate(tx) for tx in services.list_transactions(db)]


@app.post(
    "/transactions", response_model=Transaction, status_code=status.HTTP_201_CREATED
)
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
