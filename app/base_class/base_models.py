from typing import Any, Dict
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime


@as_declarative()
class Base:
    id: Any
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_json(self) -> Dict[str, Any]:
        return jsonable_encoder(self)
