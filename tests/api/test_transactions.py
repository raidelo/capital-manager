from datetime import datetime

from fastapi.testclient import TestClient

from capital_manager.core.db.models import Account, Transaction
from tests.utils import missing_data_details, transactions_to_create


def test_transactions_get_ok_empty(client: TestClient) -> None:
    resp = client.get("/transactions")
    assert resp.status_code == 200
    assert resp.json() == []


def test_transactions_get_ok_values(
    client: TestClient, transactions: list[Transaction]
) -> None:
    resp = client.get("/transactions")
    assert resp.status_code == 200
    resp_json = resp.json()
    for i, tx in enumerate(transactions):
        assert resp_json[i]["type"] == str(tx.type)
        assert resp_json[i]["amount"] == str(tx.amount)
        assert resp_json[i]["description"] == tx.description
        assert resp_json[i]["id"] == tx.id
        assert resp_json[i]["account_id"] == tx.account_id
        assert datetime.fromisoformat(resp_json[i]["created_at"]) == tx.created_at


def test_transactions_post_missing_fields(client: TestClient) -> None:
    payload = None
    resp = client.post("/transactions", json=payload)
    assert resp.status_code == 422
    assert resp.json() == missing_data_details(payload, locs=[["body"]])

    payload = {}
    resp = client.post("/transactions", json=payload)
    assert resp.status_code == 422
    assert resp.json() == missing_data_details(
        payload, locs=[["body", "type"], ["body", "amount"], ["body", "account_name"]]
    )


def test_transactions_post_ok(client: TestClient, accounts: list[Account]) -> None:
    account = accounts[0]
    transactions = transactions_to_create(account.name)

    for id, tx in enumerate(transactions, start=1):
        resp_json = client.post("/transactions", json=tx).json()

        assert resp_json["type"] == tx["type"]
        assert resp_json["amount"] == tx["amount"]
        assert resp_json["description"] == (
            tx["description"] if "description" in tx else None
        )
        assert resp_json["id"] == id
        assert resp_json["account_id"] == account.id
        assert datetime.fromisoformat(resp_json["created_at"])
