import requests

from app.core.settings import (
    WHATSAPP_ACCESS_TOKEN,
    WHATSAPP_PHONE_NUMBER_ID,
    WHATSAPP_API_VERSION,
)


class MetaWhatsAppService:
    def __init__(self):
        self.access_token = WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = WHATSAPP_PHONE_NUMBER_ID
        self.api_version = WHATSAPP_API_VERSION

    @property
    def base_url(self) -> str:
        return f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def send_text(self, *, to_phone: str, message: str) -> dict:
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message,
            },
        }

        response = requests.post(
            self.base_url,
            headers=self._headers(),
            json=payload,
            timeout=30,
        )

        data = response.json()

        if response.status_code >= 400:
            return {
                "success": False,
                "status_code": response.status_code,
                "payload": payload,
                "response": data,
            }

        message_id = None
        messages = data.get("messages") or []
        if messages:
            message_id = messages[0].get("id")

        return {
            "success": True,
            "status_code": response.status_code,
            "payload": payload,
            "response": data,
            "provider_message_id": message_id,
        }