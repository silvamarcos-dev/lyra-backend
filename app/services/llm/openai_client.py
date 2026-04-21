from openai import OpenAI
from app.core.settings import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)