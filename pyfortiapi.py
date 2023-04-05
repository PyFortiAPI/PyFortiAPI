#!/usr/bin/env Python
__author__ = "James Simpson"
__copyright__ = "Copyright 2017, James Simpson"
__license__ = "MIT"
__version__ = "0.6.0"

import requests
import logging

from requests.packages.urllib3.exceptions import InsecureRequestWarning


class FortiGate:
    def __init__(self, ipaddr, username=None, password=None, access_token=None, timeout=10, vdom="root", port="443",
                 verify=False):

        self.ipaddr = ipaddr
        self.username = username
        self.password = password
        self.access_token = access_token
        self.port = port
        self.urlbase = "https://{ipaddr}:{port}/".format(ipaddr=self.ipaddr, port=self.port)
        self.timeout = timeout
        self.vdom = vdom
        self.verify = verify
        self._session = None

    # Login / Logout Handlers
    def login(self):
        """
        Log in to FortiGate with info provided in during class instantiation


        :return: Open Session
        """
        if self._session is not None:
            return

        session = requests.session()
        if not self.verify:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        if self.access_token:
            session.headers.update({"Authorization": f"Bearer {self.access_token}"})
        else:
            url = self.urlbase + 'logincheck'
            session.post(url,
                         data='username={username}&secretkey={password}'.format(username=self.username,
                                                                                password=self.password),
                         verify=self.verify,
                         timeout=self.timeout)

            for cookie in session.cookies:
                if cookie.name == 'ccsrftoken':
                    csrftoken = cookie.value[1:-1]
                    session.headers.update({'X-CSRFTOKEN': csrftoken})

            login_check = session.get(self.urlbase + "api/v2/cmdb/system/vdom")
            login_check.raise_for_status()

        self._session = session

        return session

    # Returns an existing session or creates a new one
    def _get_session(self) -> requests.Session:
        if not self._session:
            self.login()
        return self._session

    def logout(self, session):
        """
        Log out of device

        :param session: Session created by login method

        :return: None
        """
        if self._session is None:
            return

        if not self.access_token:
            url = self.urlbase + 'logout'
            self._session.get(url, verify=self.verify, timeout=self.timeout)
            logging.info("Session logged out.")

        self._session = None

    # General Logic Methods
    def does_exist(self, object_url):
        """
        GET URL to assert whether it exists within the firewall

        :param object_url: Object to locate

        :return: Bool - True if exists, False if not
        """
        session = self._get_session()
        request = session.get(object_url, verify=self.verify, timeout=self.timeout, params='vdom=' + self.vdom)

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
        if self._session is None:
            self.login()

        request = self._session.get(url, verify=self.verify, timeout=self.timeout, params='vdom=' + self.vdom)
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
        if self._session is None:
            self.login()

            result = self._session.put(url, data=data, verify=self.verify, timeout=self.timeout,
                                       params='vdom=' + self.vdom).status_code
            return result


    def post(self, url, data):
        """
        Perform POST operation on provided URL

        :param url: Target of POST operation
        :param data: JSON data. MUST be a correctly formatted string. e.g. "{'key': 'value'}"

        :return: HTTP status code returned from POST operation
        """

        if self._session is None:
            self.login()

        result = self._session.post(url, data=data, verify=self.verify, timeout=self.timeout,
                                    params='vdom=' + self.vdom).status_code
        return result


    def delete(self, url):
        """
      Perform DELETE operation on provided URL

      :param url: Target of DELETE operation

      :return: HTTP status code returned from DELETE operation
      """
        if self._session is None:
            self.login()

        result = self._session.delete(url, verify=self.verify, timeout=self.timeout, params='vdom=' + self.vdom).status_code
        return result
  


#Firewall Configuration File Download
    
        def download_config(self, destination='file', scope='global', file_format='fos', enc_password=None,
                        password_mask=None):
        """
                config_file = device.download_config()
                Download the configuration file and save it in the current directory with the format "hostname.conf".
               :param enc_password: Optional encryption password for the configuration file.
               :param password_mask: Optional flag to mask passwords in the configuration file.
               :return: None
        """
        # Get the system status to obtain the hostname
        system_status_url = f"{self.urlbase}api/v2/monitor/system/status"
        system_status = self.get(system_status_url)
        hostname = system_status.get("hostname", "unknown_hostname")

        # Download the configuration file
        config_url = f"{self.urlbase}api/v2/monitor/system/config/backup"
        request_params = {
            'destination': 'file',
            'scope': 'global',
            'file_format': 'fos',
            'password_mask': str(password_mask).lower()
        }
        if enc_password:
            request_params['enc_password'] = enc_password

        session = self._get_session()
        response = session.get(config_url, params=request_params, verify=self.verify, timeout=self.timeout)

        # Save the configuration file
        config_file_name = f"{hostname}.conf"
        with open(os.path.join(os.getcwd(), config_file_name), "wb") as config_file:
            config_file.write(response.content)

        print(f"Configuration file saved as {config_file_name}")
        
        

    # Firewall Address Methods
    def get_firewall_address(self, specific=False, filters=False):
        """
        Get address object information from firewall

        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        :param filters: If provided, the raw filter is appended to the API call.

        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/address/"
        if specific:
            api_url += specific
        elif filters:
            api_url += "?filter=" + filters
        results = self.get(api_url)
        return results

    
    def update_firewall_address(self, address, data):
        """
        Update firewall address record with provided data
    
        :param address: Address record being updated
        :param data: JSON Data with which to upate the address record
    
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/address/" + requests.utils.quote(address, safe='')
        # Check whether target object exists
        if not self.does_exist(api_url):
            logging.error('Requested address "{address}" does not exist in Firewall config.'.format(address=address))
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
    def get_address_group(self, specific=False, filters=False):
        """
        Get address group object information from firewall
    
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        :param filters: If provided, the raw filter is appended to the API call.
    
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/addrgrp/"
        if specific:
            api_url += specific
        elif filters:
            api_url += "?filter=" + filters
        results = self.get(api_url)
        return results
    
    
    def update_address_group(self, group_name, data):
        """
        Update address group with provided data
    
        :param group_name: Address group being updated
        :param data: JSON Data with which to upate the address group
    
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/addrgrp/" + group_name
        # Check whether target object already exists
        if not self.does_exist(api_url):
            logging.error('Requested address group "{group_name}" does not exist in Firewall config.'.format(
                group_name=group_name))
            return 404
        result = self.put(api_url, data)
        return result
    
    
    def create_address_group(self, group_name, data):
        """
        Create address group
    
        :param group_name: Address group to be created
        :param data: JSON Data with which to create the address group
    
        :return: HTTP Status Code.
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
    def get_service_category(self, specific=False, filters=False):
        """
        Get service category information from firewall
    
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        :param filters: If provided, the raw filter is appended to the API call.
    
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/category/"
        if specific:
            api_url += specific
        elif filters:
            api_url += "?filter=" + filters
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
            logging.error('Requested service category "{category}" does not exist in Firewall config.'.format(
                category=category))
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
    def get_service_group(self, specific=False, filters=False):
        """
        Get service group information from firewall
    
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        :param filters: If provided, the raw filter is appended to the API call.
    
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/group/"
        if specific:
            api_url += specific
        elif filters:
            api_url += "?filter=" + filters
        results = self.get(api_url)
        return results
    
    
    def update_service_group(self, group_name, data):
        """
        Update service group with provided data
    
        :param group_name: Service group being updated
        :param data: JSON Data with which to upate the service group
    
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/group/" + group_name
        # Check whether target object already exists
        if not self.does_exist(api_url):
            logging.error('Requested service group "{group_name}" does not exist in Firewall config.'.format(
                group_name=group_name))
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
    def get_firewall_service(self, specific=False, filters=False):
        """
        Get service object information from firewall
    
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
        :param filters: If provided, the raw filter is appended to the API call.
    
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/custom/"
        if specific:
            api_url += specific
        elif filters:
            api_url += "?filter=" + filters
        results = self.get(api_url)
        return results
    
    
    def update_firewall_service(self, service_name, data):
        """
        Update service with provided data
    
        :param service_name: Service  being updated
        :param data: JSON Data with which to upate the service
    
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall.service/custom/" + service_name
        # Check whether target object already exists
        if not self.does_exist(api_url):
            logging.error('Requested service "{service_name}" does not exist in Firewall config.'.format(
                service_name=service_name))
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
    def get_firewall_policy(self, specific=False, filters=False):
        """
        Get firewall policy information from firewall
    
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
            Specific can either be the policy name, or the policy ID.
        :param filters: If provided, the raw filter is appended to the API call.
    
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/policy/"
        if specific:
            if type(specific) == int:
                api_url += str(specific)
            else:
                api_url += "?filter=name==" + specific
        elif filters:
            api_url += "?filter=" + filters
        results = self.get(api_url)
        if type(results) == int:
            return results
        elif len(results) == 0:
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
            logging.error('Requested Policy ID {policy_id} does not exist in Firewall Config.'.format(
                policy_id=str(policy_id)))
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
        data = "{{'action': 'move', '{position}': {neighbour}}}".format(position=position, neighbour=neighbour)
        result = self.put(api_url, data)
        return result
    
    
    def create_firewall_policy(self, policy_id, data):
        """
        Create firewall Policy
    
        :param policy_id: ID of policy to be created
        :param data: Data with which to create policy
    
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/policy/"
        # Check whether object already exists
        if self.does_exist(api_url + str(policy_id)):
            return 424
        result = self.post(api_url, "{{'json': {data}}}".format(data=data))
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
    
    
    # SNMPv2 Community Methods
    def get_snmp_community(self, specific=False, filters=False):
        """
        Get SNMP community information from firewall
    
        :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
            Specific can either be the Community string, or its internal ID.
        :param filters: If provided, the raw filter is appended to the API call.
    
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/system.snmp/community/"
        if specific:
            if type(specific) == int:
                api_url += str(specific)
            else:
                api_url += "?filter=name==" + specific
        elif filters:
            api_url += "?filter=" + filters
        results = self.get(api_url)
        return results
    
    
    def update_snmp_community(self, community_id, data):
        """
        Update SNMP community with provided data
    
        :param community_id: ID of community  being updated
        :param data: JSON Data with which to update the community
    
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/system.snmp/community/" + str(community_id)
        # Check whether target object already exists
        if not self.does_exist(api_url):
            logging.error('Requested SNMP Community ID "{community_id}" does not exist in Firewall config.'.format(
                community_id=community_id))
            return 404
        result = self.put(api_url, data)
        return result
    
    
    def create_snmp_community(self, community_id, data):
        """
        Create SNMP community
    
        :param community_id: ID of the SNMP Community to be created
        :param data: JSON Data with which to create the SNMP community
    
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/system.snmp/community/"
        if self.does_exist(api_url + str(community_id)):
            return 424
        result = self.post(api_url, data)
        return result
    
    
    def delete_snmp_community(self, community_id):
        """
        Delete SNMP community
    
        :param community_id: ID of the SNMP Community to be deleted
    
        :return: HTTP Status Code
        """
        api_url = self.urlbase + "api/v2/cmdb/system.snmp/community/" + str(community_id)
        result = self.delete(api_url)
        return result
    
    
    # ISDB read
    def get_internet_services(self, specific=False, filters=False):
        """
        Get ISDB (internet services database)
    
        :param specific: If provided, a specific object will be returned.
        :param filters: If provided, the raw filter is appended to the API call.
    
        :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlbase + "api/v2/cmdb/firewall/internet-service/"
        if specific:
            api_url += str(specific)
        elif filters:
            api_url += "?filter=" + filters
        results = self.get(api_url)
        return results
