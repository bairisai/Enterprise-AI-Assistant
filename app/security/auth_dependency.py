from fastapi.params import Depends, Header
import jwt

from app.database.session import get_db
from app.entities.user import User
from app.exceptions.auth_exceptions import InvalidTokenException
from app.repositories.user_repository import UserRepository
from app.security.jwt_handler import decode_access_token
from sqlalchemy.orm import Session

def get_current_user(authorization: str | None = Header(default=None),
                     db: Session = Depends(get_db),) -> User:
    if authorization is None or not authorization.startswith("Bearer "):
        raise InvalidTokenException("Missing or invalid authorization header")
    
    token = authorization.removeprefix("Bearer ")

    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise InvalidTokenException("Token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenException("Invalid token")
    username = payload.get("sub")
    if username is None:
        raise InvalidTokenException("Invalid token subject")
    repository = UserRepository(db)
    user = repository.get_user_by_username(username)
    if user is None:
        raise InvalidTokenException("User not found")
    return user