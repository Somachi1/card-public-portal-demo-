from pydantic import BaseModel
from typing import Optional


class Visits(BaseModel):
    lassra_id: int


class CreateVisits(BaseModel):
    visit_ip_address:str


class VisitsResponse(Visits):
    ip_address: int
    visit_count: int

    class Config:
        orm_mode = True


class LocalGovt(BaseModel):
    id:int
    name:str
    code:str


class OTPRequest(BaseModel):
    lasrra_id: str
    channel:str


class RelocateCard(BaseModel):
    lasrra_id:str
    destination_lg:str
    destination_location:str
    source_lg:str
    source_location:str
    otp:str

class CollectionCent(BaseModel):
    id:int
    name:str
    code:str
    lgCode:str
