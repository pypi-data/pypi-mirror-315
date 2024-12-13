import requests
import time
import datetime
import time
from urllib import parse


class Veracross:
    def __init__(self, config):
        self.bearer_token = None
        self.school = config["school"]
        self.token_url = f"https://accounts.veracross.com/{self.school}/oauth/token"
        self.api_base_url = f"https://api.veracross.com/{self.school}/v3/"
        self.client_id = config["client_id"]
        self.client_secret = config["client_secret"]
        self.scopes = config["scopes"]

        # Default page size
        self.page_size = 500

        # Requests Session
        self.session = requests.Session()

        # Session Headers
        self.session.headers.update({'Accept': 'application/json',
                                     'X-Page-Size': str(self.page_size)
                                     })

        # OAuth Token Expired
        self.token_expire_time = datetime.datetime.now() - datetime.timedelta(days=1)

        # Rate limit defaults
        self.rate_limit_remaining = 300
        self.rate_limit_reset = 0

        # DEBUG Logs
        # When set, dump a bunch of info
        self.debug = False

    def __repr__(self):
        if self.bearer_token:
            return f"Veracross_API3 connected to {self.api_base_url}"
        else:
            return "Veracross_API3"

    def debug_log(self, text):
        """
        If debug enabled - print stuff
        :param text:
        :return:
        """
        if self.debug:
            print(text)

    def get_authorization_token(self):
        """
        Get / refresh bearer token from veracross api.
        :return: string: bearer token
        """
        s = requests.Session()

        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            payload = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials',
                'scope': ' '.join(self.scopes)
            }
            r = s.post(self.token_url, data=payload, headers=headers)
            json = r.json()

            self.bearer_token = json["access_token"]
            self.session.headers.update({'Authorization': 'Bearer ' + self.bearer_token})

            self.debug_log(f"Bearer token: {self.bearer_token}")

            return json["access_token"]
        except Exception as e:
            print(e)

    def check_rate_limit(self, headers):
        if "X-Rate-Limit-Remaining" in headers:
            self.rate_limit_remaining = int(headers["X-Rate-Limit-Remaining"])

            now = int(time.time())
            reset = int(headers["X-Rate-Limit-Reset"])
            wait = reset - now
            self.rate_limit_reset = int(wait)

            if int(headers["X-Rate-Limit-Remaining"]) < 2:
                self.debug_log("VC rate limit reached. Waiting {} seconds.".format(wait))
                time.sleep(wait)

            self.debug_log(f"X-Rate-Limit-Remaining Header: {headers['X-Rate-Limit-Remaining']}")
            self.debug_log(f"X-Rate-Limit-Reset Header: {headers['X-Rate-Limit-Reset']}")
            self.debug_log(f"This rate limit value: {self.rate_limit_remaining}")

        else:
            return False

    def pull(self, endpoint, parameters=None):
        """
        Pull requested data from veracross api.
        :return: data
        """
        self.get_authorization_token()

        if parameters:
            url = self.api_base_url + endpoint + "?" + parse.urlencode(parameters, safe=':-')
        else:
            url = self.api_base_url + endpoint

        self.debug_log(f"V-Pull URL: {url}")

        # defaults
        page = 0
        data =list()

        while True:
            try:
                # Increment Page Number
                page += 1

                r = self.session.get(url,
                                     headers={'X-Page-Number': str(page)})

                self.debug_log(f"V-Pull Page Number: {page}")
                self.debug_log(f"V-Pull HTTP Headers: {r.headers}")
                self.debug_log(f"V-Pull HTTP Status Code: {r.status_code}")

                # Handle 401
                if r.status_code == 401:
                    # Possible a scope is missing
                    self.debug_log(f"V-Pull 401: Missing Scope?")
                    self.debug_log(r.text)
                    return None

                # Handle 404
                if r.status_code == 404:
                    # Not found
                    self.debug_log(f"V-Pull 404: Not found")
                    self.debug_log(r.text)
                    return None

                if r.status_code == 200:
                    self.check_rate_limit(headers=r.headers)
                    this_data = r.json()
                    this_count = len(this_data['data'])

                    data = data + this_data['data']

                    self.debug_log("V-Pull data length: {}".format(len(data)))

                    if this_count == 0 or this_count < self.page_size:
                        return data
                else:
                    return None

            except Exception as e:
                self.debug_log(f"V-Pull Error: {e}")
                return None


