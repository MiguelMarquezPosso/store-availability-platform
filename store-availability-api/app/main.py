from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routers.availability_router import router as availability_router
from app.routers.chatbot_router import router as chatbot_router

app = FastAPI(
    title="Store Availability API",
    version="1.0.0",
    description="API for store availability metrics"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(availability_router, prefix="/api/availability", tags=["availability"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["chatbot"])