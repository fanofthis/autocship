from re import T
from .client import Client

def get_ships_info(token):
    url = "https://play1-api.cryptoships.club/api/ships/me"
    client = Client(token)
    res = client.request(url)
    if res[0] == 200:
        return res[1]
    else:
        print(f'Something went wrong: {res}')
        return None

