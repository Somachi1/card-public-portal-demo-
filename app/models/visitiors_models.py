from ..database.session import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP




class Visits(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, nullable=False)
    visit_ip_address = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
