import json
from typing import Dict
import requests
import time
from datetime import datetime, timedelta


def check_claimable(records, end_from):
    for record in records:
        if record['isClaim'] == 'false':
            date_race = datetime.strptime(record['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            if date_race <= end_from:
                return True
    return False


def claim(headers, ship_id, records, start_from, end_from):
    base_url = 'https://play1-api.cryptoships.club/api/ship-histories/claim/'
    params = {'time': start_from}
    if check_claimable(records, end_from):
        res = requests.get(base_url + ship_id, params=params, headers=headers)
        if res.status_code == 200:
            print(f"Claim success on {start_from}. Balance is {res.json()['cship']}")
        else:
            print('Something error: {}'.format(res.text))
    else:
        print(f'Nothing to claim on {start_from}.')


def read_acc_info() -> Dict[str, str]:
    with open('acc.json', 'r') as f:
        accounts = json.load(f)
    return accounts['Accounts']


def get_headers(token: str) -> Dict[str, str]:
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {0}'.format(token)
    }


def refuel_ship(headers) -> None:
    url = "https://play1-api.cryptoships.club/api/ships/refuel"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        print('Refuel successful.')
    else:
        print("Can't fuel ship: {0}".format(res.json()['message']))


def get_ships(headers):
    url = "https://play1-api.cryptoships.club/api/ships/me"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        print('Something went wrong: {0}'.format(res.text))


def racing_ships(headers, ships):
    url = "https://play1-api.cryptoships.club/api/ships/racing/"
    total_rewards = 0
    num_races = 0
    for ship in ships:
        oil = ship['oil']
        while oil > 0:
            res = requests.get(url+ship['id'], headers=headers)
            if res.status_code == 200:
                data = res.json()
                oil -= 15
                print(f"{ship['name']} {data['ship']} | Position {data['position']} | " \
                      f"{data['reward']} tokens | {data['exp']} exp.")
                total_rewards += float(data['reward'])
                num_races += 1
                time.sleep(15)
            else:
                print('Something went wrong: {0}'.format(res.text))
                time.sleep(15)
    if total_rewards > 0:
        print(f'Total reward is {total_rewards} token. Average reward is {total_rewards/num_races}')
    if num_races == 0:
        print('No ship available to race.')


def claim_reward(headers, ships: list, ndays=5):
    url = "https://play1-api.cryptoships.club/api/ship-histories/training/"
    curr = datetime.now()
    for ship in ships:
        end_from = curr - timedelta(days=5)
        start_from = curr - timedelta(days=5 + ndays)
        print(f"Start claim {ship['name']} {ship['uid']} between {start_from.strftime('%Y-%m-%d')} and {end_from.strftime('%Y-%m-%d')}")
        while start_from <= end_from:
            params = {'time': start_from.strftime("%Y-%m-%d")}
            res = requests.get(url + ship['id'], headers=headers, params=params)
            if res.status_code == 200:
                records = res.json()
                if len(records) > 0:
                    claim(headers, ship['id'], records, start_from, end_from)
            else:
                print('Something went wrong: {}'.format(res.text))
            start_from += timedelta(days=1)


if __name__ == "__main__":
    print('Starting run main code')
    accounts = read_acc_info()
    for account in accounts:
        print('Start automation play {0} with address {1}'.format(account['name'], account['address']))
        headers = get_headers(account['token'])
        refuel_ship(headers)  # refuel all ships
        ships = get_ships(headers)  # fetch all ships
        racing_ships(headers, ships)  # racing
        claim_reward(headers, ships)  # claim all reward with 0% tax

