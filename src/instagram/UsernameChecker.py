import random
import requests, time

class UsernameChecker:
    def __init__(self) -> None:
        self.endpoint = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/"
        self.count_request = 0

    def check(self, _payload):
        self.count_request += 1
        print("========= Checking Username on Instagram API attempt: "+ str(self.count_request) +" =========")
        try:
            payload = {
                'email': _payload['email'],
                'username': _payload['username'],
                'first_name': _payload['first_name'],
                'seamless_login_enabled': '1',
                #'gdpr_s': '%5B0%2C2%2C0%2Cnull%5D',
                #'client_id': 'W6mHTAAEAAHsVu2N0wGEChTQpTfn',
                'tos_version': 'eu',
                'opt_into_one_tap': 'false'
            }
            response = requests.post(self.endpoint, headers={'X-CSRFToken':'en'}, data=payload, timeout=10)
            if self.count_request > 3: return payload['username']
            if response.status_code == 429:
                time.sleep(5)
                self.check(_payload)
            return self._sanitize_response(response.json(), payload)
        except requests.exceptions.Timeout:
            print("========= Instagram API Checkusername has exceded timeout limit =========")
            return payload['username']

    def _sanitize_response(self, response, payload):
        print(response)
        if response.get('status') != 'ok':
            return payload['username']
        username_suggestions = response.get('username_suggestions', [])
        if not username_suggestions:
            return payload['username']
        rand_username = random.choice(username_suggestions)
        max_length = 24
        if 'username' in response.get('errors', []):
            username = rand_username[:max_length] if len(
                rand_username) > max_length else rand_username
        else:
            username = rand_username[:max_length] if len(
                rand_username) > max_length else rand_username
        return username
