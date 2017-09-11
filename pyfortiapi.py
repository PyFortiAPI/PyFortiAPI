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
        Log in to FortiGate with info provided in during class instantiation
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

        # Check whether login was successful
        login_check = session.get(self.urlbase + "api/v2/cmdb/system/vdom")
        login_check.raise_for_status()
        return session

    def logout(self, session):
        """
        Log out of device
        :param session: Session created by login method
        :return: None
        """
        url = self.urlbase + 'logout'
        session.get(url, verify=False, timeout=self.timeout)
        logging.info("Session logged out.")

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
    def get_address_group(self, specific=False):
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

    def update_address_group(self, group_name, data):
        """
        Update address group with provided data.
        :param group_name: Address group being updated
        :param data: JSON Data with which to upate the address group
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/addrgrp/" + group_name
        # Check whether target object already exists
        if not self.does_exist(api_url):
            logging.error(f'Requested address group "{group_name}" does not exist in Firewall config.')
            return 404
        result = self.put(api_url, data)
        return result

    def create_address_group(self, group_name, data):
        """
        Create address group
        :param group_name: Address group to be created
        :param data: JSON Data with which to create the address group
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/addrgrp/"
        if self.does_exist(api_url + group_name):
            return 424
        result = self.post(api_url, data)
        return result

    def delete_address_group(self, group_name):
        """
        Delete firewall address group
        :param group_name: Address group to be deleted
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/addrgrp/" + group_name
        result = self.delete(api_url)
        return result

    # Service Category Methods
    def get_service_category(self, specific=False):
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

    def update_service_category(self, category, data):
        """
        Update service category with provided data.
        :param category: Service category being updated
        :param data: JSON Data with which to upate the service category
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/category/" + category
        # Check whether target object already exists
        if not self.does_exist(api_url):
            logging.error(f'Requested service category "{category}" does not exist in Firewall config.')
            return 404
        result = self.put(api_url, data)
        return result

    def create_service_category(self, category, data):
        """
        Create service category
        :param category: Service category to be created
        :param data: JSON Data with which to create the service category
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/category/"
        if self.does_exist(api_url + category):
            return 424
        result = self.post(api_url, data)
        return result

    def delete_service_category(self, category):
        """
        Delete firewall service category
        :param category: Service categrory to be deleted
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/category/" + category
        result = self.delete(api_url)
        return result

    # Service Group Methods
    def get_service_group(self, specific=False):
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

    def update_service_group(self, group_name, data):
        """
        Update service group with provided data.
        :param group_name: Service group being updated
        :param data: JSON Data with which to upate the service group
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/group/" + group_name
        # Check whether target object already exists
        if not self.does_exist(api_url):
            logging.error(f'Requested service group "{group_name}" does not exist in Firewall config.')
            return 404
        result = self.put(api_url, data)
        return result

    def create_service_group(self, group_name, data):
        """
        Create service group
        :param group_name: Service group to be created
        :param data: JSON Data with which to create the service group
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/group/"
        if self.does_exist(api_url + group_name):
            return 424
        result = self.post(api_url, data)
        return result

    def delete_service_group(self, group_name):
        """
        Delete firewall service group
        :param group_name: Service categrory to be deleted
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/group/" + group_name
        result = self.delete(api_url)
        return result

    # Firewall Service Methods
    def get_firewall_service(self, specific=False):
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

    def update_firewall_service(self, service_name, data):
        """
        Update service with provided data.
        :param service_name: Service  being updated
        :param data: JSON Data with which to upate the service
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/custom/" + service_name
        # Check whether target object already exists
        if not self.does_exist(api_url):
            logging.error(f'Requested service "{service_name}" does not exist in Firewall config.')
            return 404
        result = self.put(api_url, data)
        return result

    def create_firewall_service(self, service_name, data):
        """
        Create service
        :param service_name: Service to be created
        :param data: JSON Data with which to create the service
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/custom/"
        if self.does_exist(api_url + service_name):
            return 424
        result = self.post(api_url, data)
        return result

    def delete_firewall_service(self, service_name):
        """
        Delete firewall service
        :param service_name: Service categrory to be deleted
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/custom/" + service_name
        result = self.delete(api_url)
        return result

    # Firewall Policy Methods
    def get_firewall_policy(self, specific=False):
        """
        Get firewall policy information from firewall
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        Specific can either be the policy name, or the policy ID.
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/policy/"
        if specific:
            if type(specific) == int:
                api_url += str(specific)
            else:
                api_url += "?filter=name==" + specific
        results = self.get(api_url)
        if len(results) == 0:
            return 404
        else:
            return results

    def update_firewall_policy(self, policy_id, data):
        """
        Update firewall policy with provided data
        :param policy_id: ID of firewall policy to be updated
        :param data: Data with which to update the firewall policy
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/policy/" + str(policy_id)
        # Check whether target object already exists
        if not self.does_exist(api_url):
            logging.error(f'Requested Policy ID {str(policy_id)} does not exist in Firewall Config.')
            return 404
        result = self.put(api_url, data)
        return result

    def move_firewall_policy(self, policy_id, position, neighbour):
        """
        Move firewall policy to new location
        :param policy_id: ID of firewall policy being moved
        :param position: "before" or "after"
        :param neighbour: ID of policy being used as positional reference
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/policy/" + str(policy_id)
        data = f"{{'action': 'move', '{position}': {neighbour}}}"
        result = self.put(api_url, data)
        return result

    def create_firewall_policy(self, policy_id, data):
        """
        Create Firewall Policy
        :param policy_id: ID of policy to be created
        :param data: Data with which to create policy
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/policy/"
        # Check whether object already exists
        if self.does_exist(api_url + str(policy_id)):
            return 424
        result = self.post(api_url, f"{{'json': {data}}}")
        return result

    def delete_firewall_policy(self, policy_id):
        """
        Delete firewall policy
        :param policy_id: ID of policy to be deleted
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/policy/" + str(policy_id)
        result = self.delete(api_url)
        return result
