from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.handlers.exception_handlers import register_exception_handlers
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.assistant import router as assistant_router
from app.routers.documents import router as documents_router

import logging


logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s - %(levelname)s %(name)s - %(message)s"
    )

# logger = logging.getLogger(__name__)


app = FastAPI()

register_exception_handlers(app)

app.include_router(health_router)

app.include_router(auth_router)

app.include_router(assistant_router)

app.include_router(documents_router)
