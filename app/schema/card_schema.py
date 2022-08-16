from pydantic import BaseModel
from typing import Optional


class CardInfo(BaseModel):
    first_name: str
    last_name: str
    lasrra_id: str
    status: str
    location: str
    lga:str
    isDelivered:bool


class CardInfoResponse(CardInfo):
    pass

    class Config:
        orm_mode = True
