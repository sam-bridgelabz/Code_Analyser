from app.utils.logger import AppLogger
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.utils.github_utils import fetch_github_code
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from google.api_core import exceptions as google_exceptions
from app.schemas.code_check import CodeCheckRequest
from app.utils.code_utils import json_error
from app.templates.prompts import LANGUAGE_DETECTION_PROMPT, REVIEW_PROMPT
from app.utils.code_utils import extract_json_from_model_output
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

git_router = APIRouter(prefix="/github", tags=["GitHub Code Extractor"])
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

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
    print("inside review_code_with_gemini function")
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

@git_router.post("/multi-quality-check")
def multi_quality_check(request: CodeCheckRequest):
    try:
        # Step 1: Get code based on type
        if request.type == "github":
            try:
                raw_url, code = fetch_github_code(request.content)
            except Exception as e:
                return json_error(f"Error fetching GitHub code: {str(e)}")
        elif request.type == "text":
            raw_url, code = None, request.content
        else:
            return json_error("Invalid type. Must be 'github' or 'text'.")

        if not code or code.strip() == "":
            return json_error("No code found to process.")

        # Step 2: Detect language
        try:
            language = detect_language_with_gemini(code)
        except ValueError as e:
            return json_error(str(e))

        # Step 3: Review code
        try:
            review_results = review_code_with_gemini(code, language)
        except ValueError as e:
            return json_error(str(e))

        # Step 4: Structured Success Response
        return JSONResponse(
                content = {
                    "Success_status": True,
                    "Error_details": None,
                    "Results": {
                        "Language_detected": language,
                        **review_results
                    }},
                status_code=200)

    except Exception as e:
        return json_error(f"Unexpected server error: {str(e)}")
