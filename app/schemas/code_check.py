from pydantic import BaseModel, Field

class CodeCheckRequest(BaseModel):
    content: str = Field(..., description="GitHub file URL or raw code(Json format)")
    type: str = Field(..., description="'github' for GitHub link, 'text' for raw code")
