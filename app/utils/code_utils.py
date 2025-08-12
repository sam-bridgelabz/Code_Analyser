from app.utils.logger import AppLogger
from dotenv import load_dotenv
import re
from fastapi.responses import JSONResponse
import google.generativeai as genai
import os
from google.api_core import exceptions as google_exceptions
from app.utils.github_utils import fetch_github_code
from app.templates.prompts import LANGUAGE_DETECTION_PROMPT, REVIEW_PROMPT
import json

logger = AppLogger.get_logger()

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables.")
    raise RuntimeError("GEMINI_API_KEY not found in environment variables.")
# Configure Gemini API
genai.configure(api_key=api_key)


gemini_model = genai.GenerativeModel("gemini-1.5-flash")

def json_error(error_message: str):
    return JSONResponse(
        content={
            "Success_status": False,
            "Error_details": error_message,
            "Results": None},
        status_code=400)

def extract_json_from_model_output(text: str) -> str:
    """
    Removes markdown code fences (```json ... ```).
    Returns cleaned JSON string.
    """
    # Remove leading/trailing whitespace and code fences
    cleaned = re.sub(r"^```(?:json)?\n|\n```$", "", text.strip(), flags=re.MULTILINE)
    return cleaned.strip()

def get_or_extract_code(request):
    try:
        # Step 1: Get code based on type
        if request.type == "github":
            try:
                _, code = fetch_github_code(request.content)
                return code
            except Exception as e:
                return json_error(f"Error fetching GitHub code: {str(e)}")
        elif request.type == "text":
            return request.content
        else:
            return json_error("Invalid type. Must be 'github' or 'text'.")
    except Exception as e:
        logger.error(f"Unexpected error fetching code: {str(e)}")

def detect_language_with_gemini(code: str) -> str:
    try:
        prompt = LANGUAGE_DETECTION_PROMPT.format(code=code)
        response = gemini_model.generate_content(prompt)
        logger.info(f"Detected language: {response}")
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error detecting language: {str(e)}")
        raise ValueError(f"Error detecting language: {str(e)}")

def review_code_with_gemini(code: str, language: str) -> dict:
    logger.info(f"Reviewing code for language review_code_with_gemini: {language}")
    try:

        prompt = REVIEW_PROMPT.format(language=language, code=code)

        response = gemini_model.generate_content(prompt)
        logger.info(f"Code Analysis generated")
        text_output = extract_json_from_model_output(response.text)

        try:
            parsed = json.loads(text_output)
        except json.JSONDecodeError:
            logger.error(f"Model did not return valid JSON.\nOutput was:\n{text_output}")
            raise ValueError(f"Model did not return valid JSON.\nOutput was:\n{text_output}")

        return parsed

    except google_exceptions.GoogleAPICallError as e:
        logger.error(f"Gemini API error while reviewing code: {str(e)}")
        raise ValueError(f"Gemini API error while reviewing code: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error reviewing code: {str(e)}")
        raise ValueError(f"Unexpected error reviewing code: {str(e)}")
