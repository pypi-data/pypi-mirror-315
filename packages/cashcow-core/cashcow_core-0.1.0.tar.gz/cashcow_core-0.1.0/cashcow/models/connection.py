"""Connection model definition"""

from typing import Any

from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String

from cashcow.constants import ConnectionType
from cashcow.models.base import ORMModel, TimestampMixin


class Connection(ORMModel, TimestampMixin):
    """Connection model"""

    __tablename__: str = "connections"

    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    """ID of the user"""

    active: bool = Column(Boolean, nullable=False, default=True)
    """Whether the connection is active"""
    name: str = Column(String, nullable=False)
    """Name of the connection"""
    type: ConnectionType = Column(String, nullable=False)
    """Type of the connection"""
    secret: dict[str, Any] = Column(JSON, nullable=False)
    """Secret of the connection"""
    config: dict[str, Any] = Column(JSON, nullable=False, default={})
    """Configuration of the connection"""

    def __repr__(self) -> str:
        return f"<Connection id={self.id!r} name={self.name!r}>"

    def __str__(self) -> str:
        return self.__repr__()
