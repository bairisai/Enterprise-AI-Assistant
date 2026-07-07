from fastapi import FastAPI
from app.handlers.exception_handlers import register_exception_handlers
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
import logging
from app.database.base import Base
from app.database.session import engine

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s - %(levelname)s %(name)s - %(message)s"
    )

# logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

register_exception_handlers(app)

app.include_router(health_router)

app.include_router(auth_router)

