import os
from dotenv import load_dotenv
import google.generativeai as genai
from app.utils.logger import AppLogger

logger = AppLogger.get_logger()

load_dotenv()

gemini_model = None

class GeminiContext:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_response(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response

gemini_model = GeminiContext()
logger.info("Gemini model initialized")
