import pytest
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from capital_manager.core.db.models import Account
from capital_manager.core.models.account import AccountCreate
from capital_manager.core.services.accounts import (
    create_account,
    get_account_by_id,
    get_account_by_name,
    list_accounts,
)


def test_create_account_conflict(accounts: list[Account], db: Session) -> None:
    conflicting_name = accounts[0].name
    with pytest.raises(
        ValueError, match=f"^Account '{conflicting_name}' already exists$"
    ):
        _ = create_account(
            AccountCreate(name=conflicting_name, asset="TestAsset"),
            db,
        )


def test_create_account_ok(db: Session) -> None:
    data = {"name": "TestAccount", "asset": "TestAsset"}
    account = create_account(
        AccountCreate.model_validate(data),
        db,
    )
    result = db.execute(
        select(Account).where(
            and_(Account.name == data["name"], Account.asset == data["asset"])
        )
    ).scalar_one_or_none()

    assert result is not None
    assert result == account


def test_get_account_by_id_not_found(db: Session) -> None:
    id = 50
    with pytest.raises(ValueError, match=f"^Account with id: {id} not found$"):
        _ = get_account_by_id(id, db)


def test_get_account_by_id_ok(accounts: list[Account], db: Session) -> None:
    for acc in accounts:
        account = get_account_by_id(acc.id, db)

        assert account == acc


def test_get_account_by_name_not_found(db: Session) -> None:
    name = "TestAccount"
    with pytest.raises(ValueError, match=f"^Account with name: '{name}' not found$"):
        _ = get_account_by_name(name, db)


def test_get_account_by_name_ok(accounts: list[Account], db: Session) -> None:
    for acc in accounts:
        account = get_account_by_name(acc.name, db)

        assert account == acc


def test_list_accounts(accounts: list[Account], db: Session) -> None:
    result = list_accounts(db)

    assert result == accounts
