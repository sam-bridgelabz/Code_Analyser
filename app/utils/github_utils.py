import re
import requests
from fastapi import HTTPException

def convert_to_raw_url(github_url: str) -> str:
    """
    Converts a GitHub file URL to raw format.
    Example:
    https://github.com/user/repo/blob/main/file.py
    → https://raw.githubusercontent.com/user/repo/main/file.py
    """
    pattern = r"https://github\.com/(.+)/blob/(.+)"
    match = re.match(pattern, github_url)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid GitHub file URL")
    return f"https://raw.githubusercontent.com/{match.group(1)}/{match.group(2)}"

def fetch_github_code(url: str) -> str:
    """Fetch file content from GitHub raw URL."""
    if "raw.githubusercontent.com" not in url:
        url = convert_to_raw_url(url)

    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch file from GitHub")

    return url, response.text
