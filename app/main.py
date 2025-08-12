from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.config.gemini_context_config import gemini_model
from app.utils.logger import AppLogger
from app.routes.github_code import git_router

logger = AppLogger.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("--->> Application startup")
    logger.info(f"Response from Gemini --> {gemini_model.generate_response("Hello").text}")
    yield
    logger.info("--->> Application shutdown")

app = FastAPI(title="Code Analyser ", version="1.0.0", lifespan=lifespan)

app.include_router(git_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Code Quality Analyser"}

if __name__ == "__main__":
    import logging
    # Disable Uvicorn's default handlers
    logging.getLogger("uvicorn").handlers.clear()
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.error").handlers.clear()

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None
    )
