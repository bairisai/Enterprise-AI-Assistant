from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions.auth_exceptions import UserAlreadyExistsException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_exception_handler(
        request: Request, exc: UserAlreadyExistsException
    ) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})
