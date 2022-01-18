#=================**=========================
# Function workflow:
# claim_reward -> claim -> check_claimable -> get_tax_claim
#============================================

import requests
from datetime import datetime, timedelta
from .info import get_headers
from .ship import get_ships_info


MAX_TAX = 50
STEP_TAX = 10


def claim_reward(account, ndays=1):
    url = "https://play1-api.cryptoships.club/api/ship-histories/training/"
    curr = datetime.now()
    print('========================##=====================##=====================')
    print(
        'Start claim {} - {}'.format(account['name'], account['address']))
    headers = get_headers(account['token'])
    ships = get_ships_info(account['token'])
    for ship in ships:
        # print(5 - MAX_TAX_CLAIM/10)
        end_from = curr - timedelta(days=(5-account['tax_claim']/10))
        # continue
        start_from = curr - timedelta(days=5 + ndays)
        print(
            f"Start claim {account['name']}-{ship['name']} {ship['uid']} between {start_from.strftime('%Y-%m-%d')} "
            f"and {end_from.strftime('%Y-%m-%d')}")
        while start_from <= end_from:
            params = {'time': start_from.strftime("%Y-%m-%d")}
            res = requests.get(
                url + ship['id'], headers=headers, params=params)
            if res.status_code == 200:
                records = res.json()
                if len(records) > 0:
                    claim(headers, account['name'], ship['id'], records,
                            start_from.strftime("%Y-%m-%d"))
                else:
                    print(
                        f'# No racing on {start_from.strftime("%Y-%m-%d")}')
            else:
                print('Something went wrong: {}'.format(res.text))
            start_from += timedelta(days=1)


def get_tax_claim(date_race: datetime) -> int:
    diff_date = (datetime.utcnow().date() - date_race.date()).days
    if diff_date != 5:
        tax = MAX_TAX - diff_date * STEP_TAX if MAX_TAX >= diff_date * STEP_TAX else 0
    elif date_race.hour <= (datetime.utcnow() - timedelta(days=5)).hour:
        tax = 0
    else:
        tax = -1
    return tax


def check_claimable(records: list) -> bool:
    record = records[0]
    if record['isClaim'] == 'false':
        date_race = datetime.strptime(
            record['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # print('Tax claim will be: {}%.'.format(get_tax_claim(date_race)))
        if get_tax_claim(date_race) != -1:
            return True
    return False


def claim(headers: dict, account_name: str, ship_id: str, records: list, start_from: str) -> None:
    base_url = 'https://play1-api.cryptoships.club/api/ship-histories/claim/'
    params = {'time': start_from}
    print('- Start claim on {}'.format(start_from))
    if check_claimable(records):
        res = requests.get(base_url + ship_id, params=params, headers=headers)
        if res.status_code == 200:
            #print(f"Claim success on {start_from}. Balance is {res.json()['cship']}")
            print("- Claim successful. {} Balance {} is {}".format(account_name,
                res.json()['cship']))
        else:
            print('Something error: {}'.format(res.text))
    else:
        print('# All racing claimed or no timing claim.')
