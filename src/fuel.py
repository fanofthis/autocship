from .client import Client


def refuel_ships(account: dict) -> None:
    url = "https://play1-api.cryptoships.club/api/ships/refuel"
    client = Client(account['token'])
    res = client.request(url)
    if res[0] == 200:
        print('Refuel account %s | %s successful.' % (account['name'], account['address']))
    else:
        print('Something went wrong: status_code {}, {}'.format(res[0], res[1]))
