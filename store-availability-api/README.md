# ⚡ Backend (FastAPI + Python)

## Descripción
API RESTful que procesa archivos CSV con eventos de disponibilidad de tiendas (online/offline), genera métricas y ofrece un endpoint de chatbot basado en LLM.

## Principales transformaciones
- Cálculo de duración de estados (online/offline)
- Agregaciones por tienda
- Métricas globales y por tienda

## Endpoints principales
- `GET /api/availability/stores`
- `GET /api/availability/global`
- `GET /api/availability/store/{store_id}`
- `GET /api/availability/store/{store_id}/intervals`
- `POST /api/chatbot`

## Variables de entorno (.env)

Asigna a GEMINI_API_KEY tu propia API key de Google Gemini.

```env
DATA_ZIP_URL=https://drive.google.com/uc?export=download&id=1RlX-BzLvSehEc_cwCuWmu_PhFRiNJvrE
FRONTEND_ORIGIN=http://localhost:5173
GEMINI_API_KEY=
```

## Ejecutar Backend localmente

```bash
cd store-availability-api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend: 
```bash 
http://localhost:8000
```
