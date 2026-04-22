from fastapi import APIRouter
from app.config.settings import settings
from app.repositories.data_repository import DataRepository
from app.services.availability_service import AvailabilityService
from app.services.chatbot_service import ChatbotService
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter()
availability_service = AvailabilityService(DataRepository(settings.data_zip_url))
chatbot_service = ChatbotService(availability_service)

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    return chatbot_service.answer(request)