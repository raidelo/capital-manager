from sqlalchemy import inspect

from capital_manager.core.db.base import Base
from capital_manager.core.db.session import engine


def is_db_initialized() -> bool:
    """
    Check if all tables defined in Base.metadata exist in the database.

    Returns:
        bool: True if all tables exist, False otherwise.
    """
    inspector = inspect(engine)

    return all(inspector.has_table(table.name) for table in Base.metadata.sorted_tables)
