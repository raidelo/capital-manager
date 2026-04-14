from typing import Callable, Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from capital_manager.core.db.base import Base
from capital_manager.core.db.models import Account, Transaction
from capital_manager.core.models.transaction import TransactionType
from tests.session import engine, get_db_tests
from tests.utils import add_transactions, create_accounts


def db_setup[T: Session | TestClient](
    func: Callable[[], Generator[T, None, None]],
) -> Callable[[], Generator[T, None, None]]:
    def wrapper():
        Base.metadata.create_all(bind=engine)
        yield from func()
        Base.metadata.drop_all(bind=engine)

    return wrapper


@pytest.fixture
def accounts(db: Session) -> list[Account]:
    return create_accounts(
        [
            ("TestAccount1", "TestAsset1"),
            ("TestAccount2", "TestAsset2"),
        ],
        db,
    )


@pytest.fixture
def transactions(accounts: list[Account], db: Session) -> list[Transaction]:
    return add_transactions(
        [
            (TransactionType.INCOME, "100.00", accounts[0].name, "TestDescription1"),
            (TransactionType.EXPENSE, "50.00", accounts[0].name, "TestDescription2"),
            (TransactionType.INCOME, "200.00", accounts[1].name, None),
        ],
        db,
    )


@pytest.fixture
@db_setup
def db() -> Generator[Session, None, None]:
    yield from get_db_tests()
