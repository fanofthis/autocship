from .info import get_headers
import requests


def refuel_ship(accounts: list) -> None:
    print('========================##=====================##=====================')
    for account in accounts:
        headers = get_headers(account['token'])
        url = "https://play1-api.cryptoships.club/api/ships/refuel"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            print('Refuel account %s | %s successful.' %
                  (account['name'], account['address']))
        else:
            print("Can't refuel account {0} | {1} : {2}".format(account['name'], account['address'],
                                                                res.json()['message']))