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


def refuel_ship(accounts: list) -> None:
    for account in accounts:
        print('*********************************************')
        headers = get_headers(account['token'])
        url = "https://play1-api.cryptoships.club/api/ships/refuel"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            print('Refuel account %s | %s successful.' % (account['name'], account['address']))
        else:
            print("Can't refuel account {0} | {1} : {2}".format(account['name'], account['address'],
                                                                res.json()['message']))


def get_ships(headers):
    url = "https://play1-api.cryptoships.club/api/ships/me"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        print('Something went wrong: {0}'.format(res.text))
        return None


def racing_ships(accounts: list):
    url = "https://play1-api.cryptoships.club/api/ships/racing/"
    for account in accounts:
        print('*********************************************')
        print('Start racing {} - {}'.format(account['name'], account['address']))
        headers = get_headers(account['token'])
        ships = get_ships(headers)
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
            print(f"Total reward {account['name']} is {total_rewards} token. "
                  f"Average reward is {total_rewards/num_races}")
        if num_races == 0:
            print('{} no ship available to race.'.format(account['name']))


def claim_reward(accounts: list, ndays=4):
    url = "https://play1-api.cryptoships.club/api/ship-histories/training/"
    curr = datetime.now()
    for account in accounts:
        print('*********************************************')
        print('Start claim {} - {}'.format(account['name'], account['address']))
        headers = get_headers(account['token'])
        ships = get_ships(headers)
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
    refuel_ship(accounts)
    racing_ships(accounts)
    claim_reward(accounts)
    # for account in accounts:
    #     print('Start automation play {0} with address {1}'.format(account['name'], account['address']))
    #     headers = get_headers(account['token'])
    #     refuel_ship(headers)  # refuel all ships
    #     ships = get_ships(headers)  # fetch all ships
    #     racing_ships(headers, ships)  # racing
    #     claim_reward(headers, ships)  # claim all reward with 0% tax

