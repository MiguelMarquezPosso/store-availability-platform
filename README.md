# 💻 Store Availability Dashboard

Plataforma full‑stack para monitoreo de disponibilidad de tiendas.  
Incluye un **backend RESTful en FastAPI**, un **frontend moderno en React + TypeScript**, y un **chatbot** que responde preguntas basadas únicamente en los datos procesados.

---

# 🧱 Arquitectura General

```
store-availability/
├─ store-availability-api/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ config/
│  │  │  ├─ __init__.py
│  │  │  └─ settings.py
│  │  ├─ models/
│  │  │  ├─ __init__.py
│  │  │  └─ schemas.py
│  │  ├─ repositories/
│  │  │  ├─ __init__.py
│  │  │  └─ data_repository.py
│  │  ├─ routers/
│  │  │  ├─ __init__.py
│  │  │  ├─ availability_router.py
│  │  │  └─ chatbot_router.py
│  │  ├─ services/
│  │  │  ├─ __init__.py
│  │  │  ├─ availability_service.py
│  │  │  └─ chatbot_service.py
│  ├─ .env
│  ├─ Dockerfile
│  └─ requirements.txt
│
├─ store-availability-dashboard/
│  ├─ src/
│  │  ├─ api/
│  │  │  └─ client.ts
│  │  ├─ components/
│  │  │  ├─ AvailabilityChart.tsx
│  │  │  ├─ AvailabilityTable.tsx
│  │  │  ├─ Chatbot.css
│  │  │  ├─ Chatbot.tsx
│  │  │  └─ Filters.tsx
│  │  ├─ pages/
│  │  │  ├─ Dashboard.css
│  │  │  └─ Dashboard.tsx
│  │  ├─ App.css
│  │  ├─ App.tsx
│  │  ├─ index.css
│  │  ├─ main.tsx
│  │  └─ types.ts
│  ├─ .env
│  ├─ Dockerfile
│  ├─ eslint.config.js
│  ├─ index.html
│  ├─ package.json
│  ├─ package-lock.json
│  ├─ tsconfig.app.json
│  ├─ tsconfig.json
│  ├─ tsconfig.node.json
│  ├─ vite.config.ts
│  └─ Dockerfile
│
└─ docker-compose.yml
```

---

# ⚡ BACKEND (FastAPI)

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

---

# 🚀 FRONTEND (React + TypeScript)

## Descripción
Dashboard construido con Vite + React + TypeScript.  
Incluye métricas, filtros, tabla, gráficas y chatbot.

## Variables de entorno (.env)

```env
VITE_API_BASE=http://localhost:8000
```

---

## Ejecutar Frontend localmente

```bash
cd frontend
npm install
npm run dev
```
---

# DEVOPS

## docker-compose.yml

```yaml
version: "3.9"

services:
  backend:
    build: ./backend
    container_name: store-availability-api
    env_file:
      - ./backend/.env
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    container_name: store-availability-dashboard
    env_file:
      - ./frontend/.env
    ports:
      - "5173:5173"
    depends_on:
      - backend
```

# Ejecutar Backend y Frontend localmente

```bash
docker-compose up --build
```

---

# 🧩 Chatbot

El chatbot utiliza un LLM con contexto generado a partir de los datos reales procesados.  
Si la respuesta no puede inferirse del contexto, devuelve un mensaje indicando que no hay datos suficientes.

---
