# FastAPI + Python

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints
- `GET /api/availability/stores`
- `GET /api/availability/global`
- `GET /api/availability/store/{store_id}`
- `GET /api/availability/store/{store_id}/intervals`
- `POST /api/chatbot`
