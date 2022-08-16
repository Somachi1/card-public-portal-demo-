import json
from mimetypes import init
import requests
from fastapi import Request,  HTTPException, status
from app.schema.visits_schemas import RelocateCard, OTPRequest



def is_card_valid(lasrra_id:str):
    data = {'lasrraId': lasrra_id}

    is_card_valid = requests.post(
        'https://lasrraidentityapi.azurewebsites.net/lasrra-api/V1/VerificationServices/verifyId', json=data)

    if is_card_valid != 200:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid ID Format")
    return is_card_valid.json()


def get_card_status(lasrra_id:str):
    card_status = requests.get(
        f'https://lasrracardtrackingapi.azurewebsites.net/public/cardstatus/{lasrra_id}')
    if card_status.status_code != 200:
        raise HTTPException(status_code=card_status.status_code, 
                            detail=card_status.json()['message'])
                            
    return card_status.json()


def get_card_name(lasrra_id:str):
    card_name = requests.get(
        f'https://lasrraidentityapi.azurewebsites.net/lasrra-api/V1/RetrievalServices/getidnames/{lasrra_id}')
    if card_name != 200:
        raise HTTPException(status_code=card_name.status_code, detail=card_name.json()["message"]) 
    if card_name.json()["message"] != "Match":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=card_name.json()["message"]) 
    return card_name.json()



def verifyotp(relocate_card: RelocateCard):
    verify_otp_data = {
        "lasrraId": relocate_card.lasrra_id,
        "code": relocate_card.otp
        }
        
    verify_otp = requests.post(
        "https://lasrraidentityapi.azurewebsites.net/lasrra-api/V1/2fa/verifyotp", json=verify_otp_data)

    if verify_otp.status_code !=200:
        raise HTTPException(
            status_code=verify_otp.status_code, detail= verify_otp.json()["message"])
    if verify_otp.json()["message"] == "Match":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=(verify_otp.json()["message"]) )
   
    relocate_card_data = {
            "lasrraId": relocate_card.lasrra_id,
            "DestinationCode": relocate_card.destination_lg
        }
    response = requests.post(
        "https://lasrracardtrackingapi.azurewebsites.net/public/relocatemycard", json=relocate_card_data)
    return response.json()



def get_masked_contact(lasrra_id: str):
    response = requests.get(
        f"https://lasrraidentityapi.azurewebsites.net/lasrra-api/V1/2fa/getcontactoptions/{lasrra_id}")
    data = response.json()
    return data


def requestOTP(otp_request: OTPRequest):
    data = {
        "channel": otp_request.channel,
        "lasrraId": otp_request.lasrra_id,
        "service": "LAGID"
    }
    response = requests.post(
        f"https://lasrraidentityapi.azurewebsites.net//lasrra-api/V1/2fa/requestotp", json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json()['message'])
    if response.json()['message'] != "Sent":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.json()['message'])

    return response.json()

    

