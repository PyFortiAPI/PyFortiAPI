#!/usr/bin/env Python
# Developed using Python 3.6.1

import requests
import json

# Disable requests' warnings for insecure connections

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class FortiGate():
    def __init__(self, hostname, ipaddr, username, password):

        self.hostname = hostname
        self.ipaddr = ipaddr
        self.username = username
        self.password = password

    def roll_session(self):
        session = requests.session()
        url = f'https://{self.hostname}/logincheck'

        # Login
        session.post(url, data=f'username={self.username}&secretkey={self.password}', verify=False, timeout=10)

        # Get CSRF token from cookies, add to headers
        for cookie in session.cookies:
            if cookie.name == 'ccsrftoken':
                csrftoken = cookie.value[1:-1]  # strip quotes
                session.headers.update({'X-CSRFTOKEN': csrftoken})
        return session

