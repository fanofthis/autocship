
import json
from typing import Dict, List


def get_headers(token: str) -> Dict[str, str]:
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {0}'.format(token)
    }


def read_acc_info(accounts: list = None) -> List[Dict[str, str]]:
    with open('acc.json', 'r') as f:
        data = json.load(f)
    return data['Accounts'] if not accounts else [account for account in data['Accounts'] if account['name'] in accounts]

