import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 注释掉OpenAI，或设为可选
    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_KEY", "")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    API_PORT = int(os.getenv("API_PORT", "8000"))
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))

settings = Settings()