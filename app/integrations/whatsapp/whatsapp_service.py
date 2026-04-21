from app.core.settings import (
    WHATSAPP_PROVIDER,
    WHATSAPP_API_KEY,
    WHATSAPP_API_SECRET,
    WHATSAPP_PHONE_NUMBER,
)


class WhatsAppService:
    def __init__(self):
        self.provider = WHATSAPP_PROVIDER
        self.api_key = WHATSAPP_API_KEY
        self.api_secret = WHATSAPP_API_SECRET
        self.phone_number = WHATSAPP_PHONE_NUMBER

    def send_text(self, user_id: int, phone_number: str | None, message: str) -> dict:
        """
        Serviço base. Por enquanto roda em modo mock.
        Depois podemos trocar para Twilio ou API oficial do WhatsApp.
        """

        if self.provider == "mock":
            print(
                f"[WhatsApp MOCK] user_id={user_id} "
                f"phone={phone_number} "
                f"message={message}"
            )
            return {
                "success": True,
                "provider": "mock",
                "message": "Mensagem simulada com sucesso.",
            }

        # Aqui entra a implementação real no futuro
        raise NotImplementedError(
            f"Provider de WhatsApp '{self.provider}' ainda não implementado."
        )