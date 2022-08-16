from app.database.session import Base
from sqlalchemy import Column, Integer, String

class CollectionCentres(Base):
    __tablename__ = "collection_centres"

    id = Column(Integer, primary_key=True)
    code =Column(String, nullable=False, index=True)
    name=Column(String, nullable=False, unique=True)
    localGovtCode=Column(String, nullable=False)
    
    



