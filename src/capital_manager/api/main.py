from fastapi import FastAPI

from capital_manager.core.db.models import Base
from capital_manager.core.db.session import engine

from .routers import accounts, transactions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CapitalManager API")

app.include_router(accounts.router)
app.include_router(transactions.router)


@app.get("/ping")
def ping():
    """Check API is working"""
    return {"message": "pong"}
