"""Base model definition"""

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase


class ORMModel(DeclarativeBase):
    """Base model class"""

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    """Unique identifier for the model"""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id!r}>"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ORMModel):
            return self.__class__ == other.__class__ and self.id == other.id

        return False


class PipelineORMModel(ORMModel):
    """Base model class for data models"""

    __abstract__: bool = True

    raw_id: str = Column(String)
    """Raw ID of the model"""
    raw_data: dict[str, Any] = Column(JSON)
    """Raw data of the model"""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id!r} raw_id={self.raw_id!r}>"

    def __str__(self) -> str:
        return self.__repr__()


class TimestampMixin:
    """Mixin for timestamp fields"""

    created_at: datetime = Column(DateTime, nullable=False, default=datetime.now)
    """Creation date of the model"""
    updated_at: datetime = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    """Last update date of the model"""


class MetadataMixin:
    """Mixin for metadata fields"""

    metadata: dict[str, Any] = Column(JSON, nullable=False, default={})
    """Metadata of the model"""
