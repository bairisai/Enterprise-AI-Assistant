from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.entities.user import User
from app.exceptions.auth_exceptions import UserAlreadyExistsException


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise UserAlreadyExistsException(f"User with username '{user.username}' already exists")
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def username_exists(self, username: str) -> bool:
        return self.get_user_by_username(username) is not None