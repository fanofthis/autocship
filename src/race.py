from .ship import get_ships_info
from .info import get_headers
import requests
import time


DEPLAY_PER_RACE = 20


def racing_ships(accounts: list):
    url = "https://play1-api.cryptoships.club/api/ships/racing/"
    for account in accounts:
        print('========================##=====================##=====================')
        print(
            'Start racing {} - {}'.format(account['name'], account['address']))
        headers = get_headers(account['token'])
        ships = get_ships_info(headers)
        total_rewards = 0
        num_races = 0
        for ship in ships:
            oil = ship['oil']
            while oil > 0:
                res = requests.get(url+ship['id'], headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    oil -= 15
                    print(f"{ship['name']} {data['ship']} | Position {data['position']} | "
                          f"{data['reward']} tokens | {data['exp']} exp.")
                    total_rewards += float(data['reward'])
                    num_races += 1
                    time.sleep(DEPLAY_PER_RACE)
                else:
                    print('Something went wrong: {0}'.format(res.text))
                    time.sleep(DEPLAY_PER_RACE)
        if total_rewards > 0:
            print(f"Total reward {account['name']} is {total_rewards} token. "
                  f"Average reward is {total_rewards/num_races}")
        if num_races == 0:
            print('{} no ship available to race.'.format(account['name']))