from app.core.settings import GEMINI_API_KEY, GOOGLE_API_KEY, GEMINI_MODEL

try:
    import google.generativeai as genai
except ImportError:
    genai = None


def generate_multimodal(message: str) -> dict:
    api_key = GEMINI_API_KEY or GOOGLE_API_KEY

    if not api_key or genai is None:
        return {
            "success": False,
            "provider": "gemini",
            "response": "",
            "error": "Gemini não configurado."
        }

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(message)

        return {
            "success": True,
            "provider": "gemini",
            "response": response.text,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "provider": "gemini",
            "response": "",
            "error": str(e)
        }