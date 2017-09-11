#!/usr/bin/env Python
# Developed using Python 3.6.1

import requests
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

    # Login / Logout Handlers
    def login(self):
        """
        Log in to FortiGate with info provided in __init__
        :return: Open Session
        """
        session = requests.session()
        url = self.urlbase + 'logincheck'

        # Login
        session.post(url,
                     data=f'username={self.username}&secretkey={self.password}',
                     verify=False,
                     timeout=self.timeout)

        # Get CSRF token from cookies, add to headers
        for cookie in session.cookies:
            if cookie.name == 'ccsrftoken':
                csrftoken = cookie.value[1:-1]  # strip quotes
                session.headers.update({'X-CSRFTOKEN': csrftoken})
        return session

    def logout(self, session):
        """
        Log out of device
        :param session: Session created by login method
        :return: None
        """
        url = self.urlbase + 'logout'
        session.get(url, verify=False, timeout=self.timeout)

    # General Logic Methods
    def does_exist(self, object_url):
        """
        GET URL to assert whether it exists within the firewall
        :param object_url: Object to locate
        :return: Bool - True if exists, False if not
        """
        session = self.login()
        request = session.get(object_url)
        if request.status_code == 200:
            return True
        else:
            return False

    # API Interaction Methods
    def get(self, url):
        """
        Perform GET operation on provided URL
        :param url: Target of GET operation
        :return: Request result if successful (type list), HTTP status code otherwise (type int)
        """
        session = self.login()
        request = session.get(url, verify=False, timeout=self.timeout)
        self.logout(session)
        if request.status_code == 200:
            return request.json()['results']
        else:
            return request.status_code

    def put(self, url, data):
        """
        Perform PUT operation on provided URL
        :param url: Target of PUT operation
        :param data: JSON data. MUST be a correctly formatted string. e.g. "{'key': 'value'}"
        :return: HTTP status code returned from PUT operation
        """
        session = self.login()
        result = session.put(url, data=data, verify=False, timeout=self.timeout).status_code
        self.logout(session)
        return result

    def post(self, url, data):
        """
        Perform POST operation on provided URL
        :param url: Target of POST operation
        :param data: JSON data. MUST be a correctly formatted string. e.g. "{'key': 'value'}"
        :return: HTTP status code returned from POST operation
        """
        session = self.login()
        result = session.post(url, data=data, verify=False, timeout=self.timeout).status_code
        self.logout(session)
        return result

    def delete(self, url):
        """
        Perform DELETE operation on provided URL
        :param url: Target of DELETE operation
        :return: HTTP status code returned from DELETE operation
        """
        session = self.login()
        result = session.delete(url, verify=False, timeout=self.timeout).status_code
        self.logout(session)
        return result

    # Firewall Address Methods
    def get_firewall_address(self, specific=False):
        """
        Get address object information from firewall
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/address/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results

    def update_firewall_address(self, address, data):
        """
        Update firewall address record with provided data.
        :param address: Address record being updated
        :param data: JSON Data with which to upate the address record
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/address/" + address
        # Check whether target object exists
        if not self.does_exist(api_url):
            logging.error(f'Requested address "{address}" does not exist in Firewall config.')
            return 404
        result = self.put(api_url, data)
        return result

    def create_firewall_address(self, address, data):
        """
        Create firewall address record
        :param address: Address record to be created
        :param data: JSON Data with which to create the address record
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/address/"
        # Check whether target object already exists
        if self.does_exist(api_url + address):
            return 424
        result = self.post(api_url, data)
        return result

    def delete_firewall_address(self, address):
        """
        Delete firewall address record
        :param address: Address record to be deleted
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/address/" + address
        result = self.delete(api_url)
        return result

    # Address Group Methods
    def get_address_groups(self, specific=False):
        """
        Get address group object information from firewall
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/addrgrp/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results

    # Service Category Methods
    def get_service_categories(self, specific=False):
        """
        Get service category information from firewall
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/category/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results

    # Service Group Methods
    def get_service_groups(self, specific=False):
        """
        Get service group information from firewall
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/group/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results

    # Firewall Service Methods
    def get_firewall_services(self, specific=False):
        """
        Get service object information from firewall
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/custom/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results

    # Firewall Policy Methods
    def get_firewall_policies(self, specific=False):
        """
        Get firewall policy information from firewall
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/policy/"
        if specific:
            api_url += specific
        results = self.get(api_url)
        return results


