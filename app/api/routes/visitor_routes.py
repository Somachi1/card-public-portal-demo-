import http
import json
from threading import local
from urllib import response
import requests
from fastapi import APIRouter, Request, Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import func
from openpyxl import Workbook, load_workbook
from sqlalchemy.orm import Session
from app.models import (card_info_model, visitiors_models, users_model)
from app.api.dependencies.db import get_db
import os
from app.models.collection_centres import CollectionCentres
from app.models.local_government import LocalGovernment
from app.repo.visitor_repo import visitor_repo
from app.schema.card_schema import CardInfo
from app.schema.visits_schemas import LocalGovt, OTPRequest, RelocateCard


router = APIRouter()


@router.get("/search")
async def visitor_get_status(request: Request, lasrra_id: str, db: Session = Depends(get_db)):
    is_limit_reached = visitor_repo.check_ip_limit(db, ip=request.client.host)
    # if is_limit_reached:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="You have exceeded the limit, Check back")
    visitor_repo.create_visit(db, obj_in=request.client.host)
    data = {
        'lasrraId': lasrra_id
    }

    is_card_valid = requests.post(
        'https://lasrraidentityapi.azurewebsites.net/lasrra-api/V1/VerificationServices/verifystatus', json=data)

    print(is_card_valid.status_code)

    if is_card_valid.status_code != 200:
        raise HTTPException(status_code=is_card_valid.status_code,
                            detail=is_card_valid.json()['message'])
    if is_card_valid.json()['message'] == 'FAILED':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Lasraa ID {lasrra_id} Failed Verification')

    card_status = requests.get(
        f'https://lasrracardtrackingapi.azurewebsites.net/public/cardstatus/{lasrra_id}')

    card_name = requests.get(
        f'https://lasrraidentityapi.azurewebsites.net/lasrra-api/V1/RetrievalServices/getidnames/{lasrra_id}')
    if card_name.status_code != 200:
        raise HTTPException(status_code=status)
    if card_status.status_code == 404:
        return CardInfo(
            first_name=card_name.json()['firstName'],
            last_name=card_name.json()['surname'],
            lasrra_id=lasrra_id,
            status=f'No card status for {lasrra_id}',
            location="N/A",
            lga="N/A",
            isDelivered=False
        )

    if card_status.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'No card status for {lasrra_id}')

    LGA = db.query(LocalGovernment).filter(
        LocalGovernment.code == card_status.json()['lgaCode']).first()
    collection_center = db.query(CollectionCentres).filter(
        CollectionCentres.code == card_status.json()['locationCode']).first()

    return CardInfo(
        first_name=card_name.json()['firstName'],
        last_name=card_name.json()['surname'],
        lasrra_id=lasrra_id,
        status=card_status.json()['status'],
        location=collection_center.name,
        lga=LGA.name,
        isDelivered=card_status.json()['status'].startswith("Delivered"),
    )


@router.post('/relocate_card')
def relocate_my_card(relocate_card: RelocateCard, db: Session = Depends(get_db)):
    verify_otp_data = {
        "lasrraId": relocate_card.lasrra_id,
        "code": relocate_card.otp

    }
    print(verify_otp_data)
    verify_otp = requests.post(
        "https://lasrraidentityapi.azurewebsites.net/lasrra-api/V1/2fa/verifyotp", json=verify_otp_data)
    if verify_otp.status_code != 200:
        print(verify_otp.json())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="OTP Verification Failed")
    source_lga = db.query(LocalGovernment).filter(
        LocalGovernment.name == relocate_card.source_lg).first()
    print(source_lga)
    source_location = db.query(CollectionCentres).filter(
        CollectionCentres.name == relocate_card.source_location).first()
    relocate_card_data = {
        "lasrraId": relocate_card.lasrra_id,
        "fromLGACode": source_lga.code,
        "fromLocationCode": source_location.code,
        "DestinationLGACode": relocate_card.destination_location,
        "DestinationLocationCode": relocate_card.destination_lg

    }
    print(relocate_card_data)
    response = requests.post(
        "https://lasrracardtrackingapi.azurewebsites.net/public/relocatemycard", json=relocate_card_data)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=response.json())
    return response.json()


@router.get("/get_masked_contact_details")
def get_masked_contact(lasrra_id: str):
    response = requests.get(
        f"https://lasrraidentityapi.azurewebsites.net/lasrra-api/V1/2fa/getcontactoptions/{lasrra_id}")
    data = response.json()
    return data


@router.post("/requestOTP")
def requestOTP(otp_request: OTPRequest):
    data = {
        "channel": otp_request.channel,
        "lasrraId": otp_request.lasrra_id,
        "service": "LAGID"
    }
    response = requests.post(
        f"https://lasrraidentityapi.azurewebsites.net//lasrra-api/V1/2fa/requestotp", json=data)

    data = response.json()
    if data['code'] != "00":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Something went wrong")
    return {"message": "OTP Sent Successfully"}
