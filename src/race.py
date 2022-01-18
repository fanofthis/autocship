from .ship import get_ships_info
from .info import get_headers
import requests
import time
from .client import Client


DEPLAY_PER_RACE = 15


def racing_ships(account: dict):
    url = "https://play1-api.cryptoships.club/api/ships/racing/"
    print('========================##=====================##=====================')
    print(
        'Start racing {} - {}'.format(account['name'], account['address']))
    client = Client(account['token'])
    ships = get_ships_info(account['token'])
    if ships:
        total_rewards = 0
        num_races = 0
        for ship in ships:
            total_rewards_ship = 0
            ship_raced = 0
            oil = ship['oil']
            while oil > 0:
                res = client.request(url + ship['id'])
                if res[0] == 200:
                    data = res[1]
                    oil -= 15
                    print(f"- {account['name']}-{ship['name']} {data['ship']} | Position {data['position']} | "
                            f"{data['reward']} tokens | {data['exp']} exp.")
                    total_rewards_ship += float(data['reward'])
                    total_rewards += float(data['reward'])
                    ship_raced += 1
                    num_races += 1
                    time.sleep(DEPLAY_PER_RACE)
                else:
                    print('Something went wrong: {0}'.format(res))
                    time.sleep(DEPLAY_PER_RACE)
            if ship_raced > 0:
                print(f"# {account['name']} -{ ship['name']}: Total rewards {total_rewards_ship} tokens - AVG {total_rewards_ship/ship_raced} tokens.")
        if total_rewards > 0:
            print(f"# Total reward {account['name']} is {total_rewards} token. "
                    f"Average reward is {total_rewards/num_races}")
        if num_races == 0:
            print('{}-There are no ships available to race.'.format(account['name']))
    else:
        print(f"{account['name']} - Failed to fetch ships.")