import requests


def search_web(query: str) -> dict:
    try:
        url = "https://duckduckgo.com/?q=" + query.replace(" ", "+") + "&format=json"

        response = requests.get(url)
        data = response.json()

        return {
            "answer": data.get("AbstractText", ""),
            "source": data.get("AbstractURL", "")
        }

    except Exception as e:
        print("Erro na busca web:", e)
        return {
            "answer": "",
            "source": ""
        }