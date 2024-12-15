"""User model definition"""

from sqlalchemy import Column, String

from cashcow.models.base import ORMModel


class User(ORMModel):
    """User model"""

    __tablename__: str = "users"

    email: str = Column(String, nullable=False)
    """Email of the user"""
    password: str = Column(String, nullable=False)
    """Password of the user"""

    def __repr__(self) -> str:
        return f"<User {self.email!r}>"

    def __str__(self) -> str:
        return self.__repr__()
