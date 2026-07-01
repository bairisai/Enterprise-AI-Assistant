from fastapi import FastAPI
from app.config import APPLICATION_NAME, APPLICATION_VERSION

app = FastAPI()

@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "application": APPLICATION_NAME, "application_version": APPLICATION_VERSION}
