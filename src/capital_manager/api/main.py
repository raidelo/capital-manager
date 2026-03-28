from fastapi import FastAPI, HTTPException, status

from capital_manager.core import services
from capital_manager.core.models.account import Account, AccountCreate
from capital_manager.core.models.transaction import Transaction, TransactionCreate

app = FastAPI(title="CapitalManager API")


@app.get("/ping")
def ping():
    """Check API is working"""
    return {"message": "pong"}


# -------- ACCOUNT ENDPOINTS --------


@app.get("/accounts", response_model=list[Account])
def list_accounts() -> list[Account]:
    """List all accounts"""
    return services.list_accounts()


@app.post("/accounts", response_model=Account, status_code=status.HTTP_201_CREATED)
def create_account(account: AccountCreate) -> Account:
    """Create a new account"""
    try:
        return services.create_account(data=account)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))


# -------- TRANSACTION ENDPOINTS --------


@app.get("/transactions", response_model=list[Transaction])
def list_transactions() -> list[Transaction]:
    """List all transactions"""
    return services.list_transactions()


@app.post(
    "/transactions", response_model=Transaction, status_code=status.HTTP_201_CREATED
)
def add_transaction(transaction: TransactionCreate) -> Transaction:
    """Add a transaction"""
    try:
        return services.add_transaction(data=transaction)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
