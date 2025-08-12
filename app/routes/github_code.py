from app.utils.logger import AppLogger
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas.code_check import CodeCheckRequest
from app.utils.code_utils import get_or_extract_code
from app.utils.code_utils import json_error
from app.utils.code_utils import review_code_with_gemini

logger = AppLogger.get_logger()

git_router = APIRouter(prefix="/code-analyser", tags=["GitHub/Raw Code Analyser"])

@git_router.post("/code-quality-check")
def code_quality_check(request: CodeCheckRequest):
    try:
        # Step 1: Get code based on type
        # if request.type == "github":
        #     try:
        #         raw_url, code = fetch_github_code(request.content)
        #     except Exception as e:
        #         return json_error(f"Error fetching GitHub code: {str(e)}")
        # elif request.type == "text":
        #     raw_url, code = None, request.content
        # else:
        #     return json_error("Invalid type. Must be 'github' or 'text'.")
        code = get_or_extract_code(request)

        if not code or code.strip() == "":
            return json_error("No code found to process.")

        # Step 2: Detect language
        # try:
        #     language = detect_language_with_gemini(code)
        # except ValueError as e:
        #     return json_error(str(e))

        # Step 3: Review code
        try:
            review_results = review_code_with_gemini(code, "Java")
        except ValueError as e:
            return json_error(str(e))

        # Step 4: Structured Success Response
        return JSONResponse(
                content = {
                    "Success_status": True,
                    "Error_details": None,
                    "Results": {
                        # "Language_detected": language,
                        **review_results
                    }},
                status_code=200)

    except Exception as e:
        return json_error(f"Unexpected server error: {str(e)}")
