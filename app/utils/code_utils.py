import re
from fastapi.responses import JSONResponse

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
