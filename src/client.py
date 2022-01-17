import requests

class Client:

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(token)
        }
    
    def __build_request(self, url, payload):
        return requests.get(url, headers=self.headers, params=payload)
    
    def __build_response(self, res):
        if res.status_code == 200:
            return res.status_code, res.json()
        else:
            return res.status_code, res.text

    def request(self, url, payload=None):
        return self.__build_response(self.__build_request(url, payload))