from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.brain.brain import process_user_message

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = process_user_message(request.message)

    return ChatResponse(
        user_message=request.message,
        detected_intent=result["detected_intent"],
        lyra_response=result["lyra_response"]
    )