#!/usr/bin/env Python
# Developed using Python 3.6.1

import requests
import json
import logging

# Disable requests' warnings for insecure connections
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class FortiGate:
    def __init__(self, hostname, ipaddr, username, password, timeout=10):

        self.hostname = hostname
        self.ipaddr = ipaddr
        self.username = username
        self.password = password
        self.urlbase = f"https://{self.ipaddr}/"
        self.timeout = timeout

    def login(self):
        session = requests.session()
        url = self.urlbase + 'logincheck'

        # Login
        session.post(url, data=f'username={self.username}&secretkey={self.password}', verify=False, timeout=self.timeout)

        # Get CSRF token from cookies, add to headers
        for cookie in session.cookies:
            if cookie.name == 'ccsrftoken':
                csrftoken = cookie.value[1:-1]  # strip quotes
                session.headers.update({'X-CSRFTOKEN': csrftoken})
        return session

    def logout(self, session):
        url = self.urlbase + 'logout'
        session.get(url, verify=False, timeout=self.timeout)

    def does_exist(self, object_url):
        session = self.login()
        request = session.get(object_url)
        if request.status_code == 200:
            return True
        else:
            return False

    def get(self, url):
        session = self.login()
        results = session.get(url, verify=False, timeout=self.timeout).json()['results']
        self.logout(session)
        return results

    def put(self, url, data):
        session = self.login()
        results = session.put(url, data=data, verify=False, timeout=self.timeout).status_code
        self.logout(session)
        return results

    def get_firewall_address(self, specific=False):
        api_url = self.urlbase + "api/v2/cmdb/firewall/address/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results

    def get_firewall_address_groups(self, specific=False):
        api_url = self.urlbase + "api/v2/cmdb/firewall/addrgrp/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results

    def get_firewall_service_categories(self, specific=False):
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/category/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results

    def get_firewall_service_groups(self, specific=False):
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/group/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results

    def get_firewall_services(self, specific=False):
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/custom/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results

    def get_firewall_policies(self, specific=False):
        api_url = self.urlbase + "api/v2/cmdb/firewall/policy/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results

    def update_firewall_address(self, address, data):
        api_url = self.urlbase + "api/v2/cmdb/firewall/address/" + address
        # Check whether target object exists
        if not self.does_exist(api_url):
            logging.error(f'Requested address "{address}" does not exist in Firewall config.')
            return 404
        result = self.put(api_url, data)
        return result
