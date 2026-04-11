from datetime import datetime
from typing import Any

from fastapi.testclient import TestClient

from capital_manager.core.db.models import Account, Transaction
from tests.utils import calculate_balance_from_transactions, missing_data_details


def test_accounts_get_ok_empty(client: TestClient) -> None:
    resp = client.get("/accounts")
    assert resp.status_code == 200
    assert resp.json() == []


def test_accounts_get_ok_values(client: TestClient, accounts: list[Account]) -> None:
    resp = client.get("/accounts")
    assert resp.status_code == 200
    resp_json = resp.json()
    for i, acc in enumerate(accounts):
        assert resp_json[i]["name"] == acc.name
        assert resp_json[i]["asset"] == acc.asset
        assert resp_json[i]["id"] == acc.id
        assert datetime.fromisoformat(resp_json[i]["created_at"]) == acc.created_at


def test_accounts_post_missing_fields(client: TestClient) -> None:
    variants: list[tuple[None | dict[str, str], list[list[str]]]] = [
        (None, [["body"]]),
        ({}, [["body", "name"], ["body", "asset"]]),
        ({"name": "TestAccount"}, [["body", "asset"]]),
        ({"asset": "TestAsset"}, [["body", "name"]]),
    ]

    for payload, loc in variants:
        resp = client.post("/accounts", json=payload)
        assert resp.status_code == 422
        assert resp.json() == missing_data_details(payload, locs=loc)


def test_accounts_post_conflict(client: TestClient, accounts: list[Account]) -> None:
    conflicting_name = accounts[0].name
    payload = {"name": conflicting_name, "asset": "TestAsset"}
    resp = client.post("/accounts", json=payload)
    assert resp.status_code == 409
    assert resp.json() == {"detail": f"Account '{conflicting_name}' already exists"}


def test_accounts_post_ok(client: TestClient) -> None:
    payload = {"name": "TestAccount", "asset": "TestAsset"}
    resp = client.post("/accounts", json=payload)
    assert resp.status_code == 201
    resp_json = resp.json()
    assert resp_json["name"] == payload["name"]
    assert resp_json["asset"] == payload["asset"]
    assert resp_json["id"] == 1
    assert datetime.fromisoformat(resp_json["created_at"])


def balance_asserts(
    client: TestClient, params: dict[str, str], status_code: int, desired_response: Any
) -> None:
    resp = client.get("/accounts/balance", params=params)
    assert resp.status_code == status_code
    assert resp.json() == desired_response


def not_found_with_id_response(id: Any):
    return {"detail": f"Account with id: {id} not found"}


def not_found_with_name_response(name: Any):
    return {"detail": f"Account with name: '{name}' not found"}


def not_found_with_id_and_name_response(id: Any, name: Any):
    return {"detail": f'Account with id: {id} and name: "{name}" not found'}


def error_parsing_id_response(
    input: str,
) -> dict[str, list[dict[str, str | list[str]]]]:
    return {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["query", "account_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": input,
            }
        ]
    }


def test_accounts_balance_all_cases(
    client: TestClient,
    accounts: list[Account],
    transactions: list[Transaction],
) -> None:
    account_to_get_balance_from = accounts[0]

    balance = calculate_balance_from_transactions(
        account_to_get_balance_from, transactions
    )

    empty_account_name_response = {
        "detail": "Must provide a non-empty string for account_name"
    }
    empty_query_response = {"detail": "Must provide account_id or account_name"}
    desired_response = {
        "balance": str(balance),
        "asset": account_to_get_balance_from.asset,
    }

    existent_id = str(account_to_get_balance_from.id)
    existent_name = account_to_get_balance_from.name

    non_existent_id = "100"
    non_existent_name = "InvalidAccount"

    incorrect_id_format = ""

    existent_account_id = [
        (
            {"account_id": existent_id, "account_name": existent_name},
            200,
            desired_response,
        ),
        (
            {"account_id": existent_id, "account_name": non_existent_name},
            404,
            not_found_with_id_and_name_response(existent_id, non_existent_name),
        ),
        (
            {"account_id": existent_id, "account_name": ""},
            400,
            empty_account_name_response,
        ),
        (
            {"account_id": existent_id},
            200,
            desired_response,
        ),
    ]
    non_existent_account_id = [
        (
            {"account_id": non_existent_id, "account_name": existent_name},
            404,
            not_found_with_id_and_name_response(non_existent_id, existent_name),
        ),
        (
            {"account_id": non_existent_id, "account_name": non_existent_name},
            404,
            not_found_with_id_and_name_response(non_existent_id, non_existent_name),
        ),
        (
            {"account_id": non_existent_id, "account_name": ""},
            400,
            empty_account_name_response,
        ),
        (
            {"account_id": non_existent_id},
            404,
            not_found_with_id_response(non_existent_id),
        ),
    ]
    empty_account_id = [
        (
            {"account_id": incorrect_id_format, "account_name": existent_name},
            422,
            error_parsing_id_response(incorrect_id_format),
        ),
        (
            {"account_id": incorrect_id_format, "account_name": non_existent_name},
            422,
            error_parsing_id_response(incorrect_id_format),
        ),
        (
            {"account_id": incorrect_id_format, "account_name": ""},
            422,
            error_parsing_id_response(incorrect_id_format),
        ),
        (
            {"account_id": incorrect_id_format},
            422,
            error_parsing_id_response(incorrect_id_format),
        ),
    ]
    absent_account_id = [
        (
            {"account_name": existent_name},
            200,
            desired_response,
        ),
        (
            {"account_name": non_existent_name},
            404,
            not_found_with_name_response(non_existent_name),
        ),
        (
            {"account_name": ""},
            400,
            empty_account_name_response,
        ),
        (
            {},
            400,
            empty_query_response,
        ),
    ]

    for params, status_code, response in [
        *existent_account_id,
        *non_existent_account_id,
        *empty_account_id,
        *absent_account_id,
    ]:
        balance_asserts(client, params, status_code, response)
