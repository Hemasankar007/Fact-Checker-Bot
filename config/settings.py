import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = "gemini-1.5-flash"
    TEMPERATURE = 0.7
    MAX_TOKENS = 500
    SEARCH_MAX_RESULTS = 5
