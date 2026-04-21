from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Mensagem enviada pelo usuário")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Quero criar uma IA para atendimento imobiliário"
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    user_message: str
    detected_intent: str
    lyra_response: str