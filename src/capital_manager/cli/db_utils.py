import typer

from capital_manager.core.db_utils import is_db_initialized


def ensure_db_initialized() -> None:
    """
    Ensure that the database is initialized. If not, print an error message
    and exit the CLI.

    Raises:
        typer.Exit: Exits with code 1 if the database is not initialized.
    """
    tables_exist = is_db_initialized()

    if not tables_exist:
        print("Error: Database not initialized. Run 'capman init-db' first.")
        raise typer.Exit(code=1)
