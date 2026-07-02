from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
import logging

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s - %(levelname)s %(name)s - %(message)s"
    )

# logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(health_router)

app.include_router(auth_router)

