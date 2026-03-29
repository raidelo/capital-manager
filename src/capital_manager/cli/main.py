import typer
import uvicorn

from capital_manager.core.db.base import Base
from capital_manager.core.db.session import engine
from capital_manager.core.db_utils import is_db_initialized

from .account import app as account_app
from .transaction import app as transaction_app

app = typer.Typer()

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


@app.command("init-db")
def cli_init_db():
    """Initialize the database tables"""
    if is_db_initialized():
        print("Database already initialized.")
    else:
        Base.metadata.create_all(bind=engine)
        print("Database initialized.")


if __name__ == "__main__":
    app()
