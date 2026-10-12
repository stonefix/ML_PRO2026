# ML_PRO2026

docker compose exec db psql ‐U postgres ‐d churn ‐c "SELECT request_id, score, latency_ms, status_code FROM predictions;"
curl ‐i ‐X POST localhost:8000/v1/predict‐H "Content‐Type: application/json"‐d "{\"attack\":‐1}"
curl localhost:8000/health
curl -X POST localhost:8000/v1/predict -H "Content-Type: application/json" -d @good.json