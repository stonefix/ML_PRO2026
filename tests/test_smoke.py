def test_predict_smoke(client, good_row):
    r = client.post("/v1/predict", json=good_row)
    assert r.status_code == 200
    body = r.json()
    assert 0.0 <= body["score"] <= 1.0
    assert isinstance(body["is_legendary"], bool)
    assert body["latency_ms"] >= 0
    assert body["model_version"]


def test_predict_handles_percentage_male(client, good_row):
    r = client.post("/v1/predict", json={**good_row, "percentage_male": None})
    assert r.status_code == 200


def test_batch_and_single_agree(client, good_row):
    s1 = client.post("/v1/predict", json=good_row).json()["score"]
    s2 = client.post("/v1/predict", json=good_row).json()["score"]
    assert abs(s1 - s2) < 1e-12

def test_boundary_values_min_acceptable(client):
    payload = {
        "attack": 1,
        "defense": 1,
        "hp": 1,
        "sp_attack": 1,
        "sp_defense": 1,
        "speed": 1,
        "height_m": 0.01,  # gt=0
        "weight_kg": 0.01,  # gt=0
        "percentage_male": 0,
        "generation": 1,
        "type": "fire"
    }
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 200
