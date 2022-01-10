import requests

def get_ships_info(headers: dict):
    url = "https://play1-api.cryptoships.club/api/ships/me"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        print('Something went wrong: {0}'.format(res.text))
        return None