import requests


async def get_card_name(lasrra_id: str):
    response =  requests.get(
        f'https://lasrraidentityapi.azurewebsites.net/lasrra-api/V1/RetrievalServices/getidnames/{lasrra_id}')
    print('hello from request')
    return response
