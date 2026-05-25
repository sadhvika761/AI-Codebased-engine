import google.generativeai as genai
import os
from config import settings

key = settings.gemini_api_key or os.getenv("GEMINI_API_KEY")
genai.configure(api_key=key)

for m in genai.list_models():
    if "flash" in m.name or "pro" in m.name:
        print(m.name)
