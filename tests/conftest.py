import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as _activities


@pytest.fixture
def client():
    """Provide a TestClient and restore the global `activities` after each test.

    This keeps tests isolated from each other by deep-copying the in-memory
    data structure before the test and restoring it afterwards.
    """
    original = copy.deepcopy(_activities)
    with TestClient(app) as c:
        yield c
    _activities.clear()
    _activities.update(original)
