from typing import Generator

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

TEST_SQLALCHEMY_DB_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_SQLALCHEMY_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionMaker = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db_tests() -> Generator[Session, None, None]:
    with TestSessionMaker() as session:
        yield session
