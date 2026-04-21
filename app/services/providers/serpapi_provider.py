import requests
from app.core.settings import SERPAPI_API_KEY


def search(query: str) -> dict:
    if not SERPAPI_API_KEY:
        return {
            "success": False,
            "provider": "serpapi",
            "response": "",
            "source": "",
            "error": "SERPAPI_API_KEY não configurada."
        }

    try:
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "hl": "pt-BR",
            "gl": "br"
        }

        response = requests.get(url, params=params, timeout=20)
        data = response.json()

        if "organic_results" in data and data["organic_results"]:
            first = data["organic_results"][0]

            text = first.get("snippet") or first.get("title") or ""
            source = first.get("link") or ""

            return {
                "success": True,
                "provider": "serpapi",
                "response": text,
                "source": source,
                "error": None
            }

        return {
            "success": False,
            "provider": "serpapi",
            "response": "",
            "source": "",
            "error": "Nenhum resultado encontrado."
        }

    except Exception as e:
        return {
            "success": False,
            "provider": "serpapi",
            "response": "",
            "source": "",
            "error": str(e)
        }