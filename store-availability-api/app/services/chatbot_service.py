import os
import json
import google.generativeai as genai
from app.models.schemas import ChatRequest, ChatResponse
from app.services.availability_service import AvailabilityService


class ChatbotService:
    def __init__(self, availability_service: AvailabilityService):
        self.availability_service = availability_service
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-flash-latest")

    def answer(self, request: ChatRequest) -> ChatResponse:
        stores = self.availability_service.list_store_ids()

        if request.store_id:
            store_summary = self.availability_service.summarize_store(
                request.store_id, request.from_date, request.to_date, sample_size=80
            )
            context = {"store_summary": store_summary}
        else:
            global_metrics = self.availability_service.get_global_metrics(
                request.from_date, request.to_date
            )
            sample_stores = stores[:3]
            sample_summaries = [
                self.availability_service.summarize_store(s, request.from_date, request.to_date, sample_size=40)
                for s in sample_stores
            ]
            context = {
                "global_metrics": global_metrics.model_dump(),
                "sample_stores": sample_summaries
            }

        system_prompt = (
            "Eres analista de datos. Responde usando SOLO el contexto proporcionado. "
            "Si no hay datos, di explícitamente que no se puede responder."
        )

        prompt = (
            f"{system_prompt}\n\n"
            f"Context (JSON): {json.dumps(context)}\n\n"
            f"Question: {request.question}"
        )

        response = self.model.generate_content(prompt)
        answer = response.text or "No puedo responder con el contexto actual."

        return ChatResponse(answer=answer, sources=["gemini"])