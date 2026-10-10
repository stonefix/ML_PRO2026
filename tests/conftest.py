import pytest
from fastapi.testclient import TestClient

from churn.service.app import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def good_row():
    return {
        "attack": 134,
        "defense": 95,
        "height_m": 2.2,
        "hp": 91,
        "percentage_male": 50.0,
        "sp_attack": 100,
        "sp_defense": 100,
        "speed": 80,
        "weight_kg": 210.0,
        "generation": 1,
        "type": "Dragon"
    }
