import json
from pathlib import Path
from locust import HttpUser, task, between

GOOD_PAYLOAD_PATH = Path(__file__).parent / "good.json"

with open(GOOD_PAYLOAD_PATH, "r", encoding="utf-8") as f:
    VALID_PREDICT_PAYLOAD = json.load(f)


class PokemonUser(HttpUser):
    wait_time = between(1, 3)

    @task(weight=5)
    def predict_pokemon(self):
        with self.client.post(
            "/v1/predict",
            json=VALID_PREDICT_PAYLOAD,
            name="/v1/predict",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Predict failed: {response.status_code}")

    @task(weight=1)
    def check_health(self):
        with self.client.get(
            "/health",
            name="/health",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Health check failed: {response.status_code}")