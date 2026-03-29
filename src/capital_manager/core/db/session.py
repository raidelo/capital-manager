from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path.home() / ".config" / "capital-manager"
DB_PATH = BASE_DIR / "data" / "database.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DB_URL)

SessionMaker = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db():
    with SessionMaker() as session:
        yield session
