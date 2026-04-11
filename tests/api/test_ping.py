from fastapi.testclient import TestClient


def test_ping(client: TestClient) -> None:
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.json() == {"message": "pong"}
