from typing import Generator

import pytest
from fastapi.testclient import TestClient

from capital_manager.api.main import app
from capital_manager.core.db.session import get_db
from tests.conftest import db_setup
from tests.session import get_db_tests


@pytest.fixture
@db_setup
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = get_db_tests
    yield TestClient(app)
    app.dependency_overrides.clear()
