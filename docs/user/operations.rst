User Operations
===============

Firewall Address Objects
------------------------


Get
~~~

To get all address objects from your device::

    >>> addresses = device.get_firewall_address()

Alternatively, this method looks for a single parameter ("specific") which can be provided to target a single object::

    >>> my_address = device.get_firewall_address('Test')

The output of this function will be a list. If you've asked for a specific address, this list will be one item long,
but will still be a list.

Each member of the list will be a python dictionary, directly mapped from the FortiGate API's JSON result. This can be
seen in the example below::

    >>> device.get_firewall_address('Test')
    [{'name': 'Test', 'q_origin_key': 'Test', 'uuid': '264b09e6-984f-51e7-5ca7-5fc5d32b3a2b', 'subnet': '10.0.0.0 255.0.0.0', 'type': 'ipmask', 'start-ip': '10.0.0.0', 'end-ip': '255.0.0.0', 'fqdn': '', 'country': '\n', 'wildcard-fqdn': '', 'cache-ttl': 0, 'wildcard': '10.0.0.0 255.0.0.0', 'comment': '', 'visibility': 'enable', 'associated-interface': '', 'color': 0, 'tags': [], 'allow-routing': 'disable'}]


Update
~~~~~~

To update an address object, you'll need to pass two parameters to the update_firewall_address function. The name of
the address object being updated, and a JSON formatted object configuration (only the fields being updated are
required)::

    >>> payload = "{'subnet': '192.168.0.0 255.255.255.0'}"
    >>> device.update_firewall_address('Test', payload)
    200
    >>> device.get_firewall_address('Test')[0]['subnet']
    '192.168.0.0 255.255.255.0'

Note: you can't just use a python dictionary as your payload. Please refer to the "424" section in
:doc:`common_issues`.

Create
~~~~~~

To create an address object, you'll need to provide two parameters to the create_firewall_address function. The name
of the address object being created ("**address**"), and a JSON formatted object configuration ("**data**")::

    >>> payload = "{'name': 'Test', 'type': 'subnet', 'subnet': '192.168.0.0 255.255.255.0'}"
    >>> device.create_firewall_address('Test', payload)
    200

Delete
~~~~~~

To delete an address object, you just need to pass the address name to the delete_firewall_address function::

    >>> device.delete_firewall_address('Test')
    200
    >>> device.get_firewall_address('Test')
    404

Address Groups
--------------

Get
~~~

To get all address groups from your device::

    >>> groups = device.get_address_group()

Alternatively, this method looks for a single parameter ("specific") which can be provided to target a single object::

    >>> my_group = device.get_address_group('Test Group')

The output of this function will be a list. If you've asked for a specific group, this list will be one item long,
but will still be a list.

Each member of the list will be a python dictionary, directly mapped from the FortiGate API's JSON result. This can be
seen in the example below::

    >>> device.get_address_group('Test Group')
    [{'name': 'Test Group', 'q_origin_key': 'Test Group', 'uuid': '505cbc26-9871-51e7-63ce-8e5b80914ff9', 'member': [{'name': 'Test', 'q_origin_key': 'Test'}], 'comment': '', 'visibility': 'enable', 'color': 0, 'tags': [], 'allow-routing': 'disable'}]

Update
~~~~~~

To update an address group, you'll need to pass two parameters to the update_address_group function. The name of
the address group being updated, and a JSON formatted object configuration (only the fields being updated are
required)::

    >>> payload = "{'member': [{'name': 'Test'}]}"
    >>> device.update_address_group('Test Group', payload)
    200
    >>> device.get_address_group('Test Group')[0]['member']
    [{'name': 'Test', 'q_origin_key': 'Test'}]


Note: you can't just use a python dictionary as your payload. Please refer to the "424" section in
:doc:`common_issues`.

Create
~~~~~~

To create an address group, you'll need to provide two parameters to the create_address_group function. The name
of the address group being created ("**group_name**"), and a JSON formatted object configuration ("**data**")::

    >>> payload = "{'name': 'Test Group', 'member': [{'name': 'Test'}]}"
    >>> device.create_address_group('Test Group', payload)
    200

Delete
~~~~~~

To delete an address group, you just need to pass the group name to the delete_address_group function::

    >>> device.delete_address_group('Test Group')
    200

Service Categories
------------------

Get
~~~

To get all service categories from your device::

    >>> categories = device.get_service_category()

Alternatively, this method looks for a single parameter ("specific") which can be provided to target a single object::

    >>> my_cat = device.get_service_category('Test Category')

The output of this function will be a list. If you've asked for a specific service category, this list will be one item
long, but will still be a list.

Each member of the list will be a python dictionary, directly mapped from the FortiGate API's JSON result. This can be
seen in the example below::

    >>> device.get_service_category('Test Category')
    [{'name': 'Test Category', 'q_origin_key': 'Test Category', 'comment': 'A category for testing.'}]

Update
~~~~~~

To update a service category, you'll need to pass two parameters to the update_service_category function. The name of
the category being updated, and a JSON formatted object configuration (only the fields being updated are required)::

    >>> payload = "{'comment': 'Test test test!'}"
    >>> device.update_service_category('Test Category', payload)
    200
    >>> device.get_service_category('Test Category')[0]['comment']
    'Test test test!'

Note: you can't just use a python dictionary as your payload. Please refer to the "424" section in
:doc:`common_issues`.

Create
~~~~~~

To create a service category, you'll need to provide two parameters to the create_service_category function. The name
of the service category being created ("**category**"), and a JSON formatted object configuration ("**data**")::

    >>> payload = "{'name': 'Test Category', 'comment': 'A category for testing.'}"
    >>> device.create_service_category('Test Category', payload)
    200

Delete
~~~~~~

To delete a service category, you just need to pass the category name to the delete_service_category function::

    >>> device.delete_service_category('Test Category')
    200

Service Groups
--------------

Get
~~~

To get all service groups from your device::

    >>> groups = device.get_service_group()

Alternatively, this method looks for a single parameter ("specific") which can be provided to target a single object::

    >>> my_group = device.get_service_group('Test Group')

The output of this function will be a list. If you've asked for a specific group, this list will be one item long,
but will still be a list.

Each member of the list will be a python dictionary, directly mapped from the FortiGate API's JSON result. This can be
seen in the example below::

    >>> device.get_service_group('Test Group')
    [{'name': 'Test Group', 'q_origin_key': 'Test Group', 'member': [{'name': 'Test', 'q_origin_key': 'Test'}], 'proxy': 'disable', 'comment': '', 'color': 0}]

Update
~~~~~~

To update a service group, you'll need to pass two parameters to the update_service_group function. The name of
the service group being updated, and a JSON formatted object configuration (only the fields being updated are
required)::

    >>> payload = "{'member': [{'name': 'Test'}]}"
    >>> device.update_service_group('Test Group', payload)
    200
    >>> device.get_service_group('Test Group')[0]['member']
    [{'name': 'Test', 'q_origin_key': 'Test'}]


Note: you can't just use a python dictionary as your payload. Please refer to the "424" section in
:doc:`common_issues`.

Create
~~~~~~

To create a service group, you'll need to provide two parameters to the create_service_group function. The name
of the service group being created ("**group_name**"), and a JSON formatted object configuration ("**data**")::

    >>> payload = "{'name': 'Test Group', 'member': [{'name': 'Test'}]}"
    >>> device.create_service_group('Test Group', payload)
    200

Delete
~~~~~~

To delete a service group, you just need to pass the group name to the delete_service_group function::

    >>> device.delete_service_group('Test Group')
    200

Firewall Service
----------------

Get
~~~

To get all firewall services from your device::

    >>> services = device.get_firewall_service()

Alternatively, this method looks for a single parameter ("specific") which can be provided to target a single object::

    >>> my_service = device.get_firewall_service('Test')

The output of this function will be a list. If you've asked for a specific group, this list will be one item long,
but will still be a list.

Each member of the list will be a python dictionary, directly mapped from the FortiGate API's JSON result. This can be
seen in the example below::

    >>> device.get_firewall_service('Test')
    [{'name': 'Test', 'q_origin_key': 'Test', 'proxy': 'disable', 'category': 'General', 'protocol': 'TCP/UDP/SCTP', 'helper': 'auto', 'iprange': '0.0.0.0', 'fqdn': '', 'protocol-number': 6, 'icmptype': '', 'icmpcode': '', 'tcp-portrange': '80', 'udp-portrange': '123', 'sctp-portrange': '', 'tcp-halfclose-timer': 0, 'tcp-halfopen-timer': 0, 'tcp-timewait-timer': 0, 'udp-idle-timer': 0, 'session-ttl': 0, 'check-reset-range': 'default', 'comment': '', 'color': 0, 'visibility': 'enable', 'app-service-type': 'disable', 'app-category': [], 'application': []}]

Update
~~~~~~

To update a firewall service, you'll need to pass two parameters to the update_firewall_service function. The name of
the firewall service being updated, and a JSON formatted object configuration (only the fields being updated are
required)::

    >>> payload = "{'tcp-portrange': '80 443'}"
    >>> device.update_firewall_service('Test', payload)
    200
    >>> device.get_firewall_service('Test')[0]['tcp-portrange']
    '80 443'

Note: you can't just use a python dictionary as your payload. Please refer to the "424" section in
:doc:`common_issues`.

Create
~~~~~~

To create a firewall service, you'll need to provide two parameters to the create_firewall_service function. The name
of the service being created ("**service_name**"), and a JSON formatted object configuration ("**data**")::

    >>> payload = "{'name': 'Test', 'category': 'General', 'tcp-portrange': '80', 'udp-portrange': '123'}"
    >>> device.create_firewall_service('Test', payload)
    200

Delete
~~~~~~

To delete a firewall service, you just need to pass the service name to the delete_firewall_service function::

    >>> device.delete_firewall_service('Test')
    200


Firewall Policy
---------------

Get
~~~

To get all firewall policies from your device::

    >>> policies = device.get_firewall_policy()

Alternatively, this method looks for a single parameter ("specific") which can be provided to target a single object.
Specific in this instance can be either a policy name, or a policy ID::

    >>> my_policy = device.get_firewall_policy('Test Policy')
    >>> my_policy = device.get_firewall_policy(500)
    >>> device.get_firewall_policy('Test Policy') == device.get_firewall_policy(500)
    True

The output of this function will be a list. If you've asked for a specific group, this list will be one item long,
but will still be a list.

Each member of the list will be a python dictionary, directly mapped from the FortiGate API's JSON result. This can be
seen in the example below::

    >>> device.get_firewall_policy(500)
    [{'policyid': 500, 'q_origin_key': 500, 'name': 'Test Policy', 'uuid': '9b70d28a-990f-51e7-95ef-dd4f2065b5ce', 'srcintf': [{'name': 'lan', 'q_origin_key': 'lan'}], 'dstintf': [{'name': 'wan', 'q_origin_key': 'wan'}], 'srcaddr': [{'name': 'all', 'q_origin_key': 'all'}], 'dstaddr': [{'name': 'Test', 'q_origin_key': 'Test'}], 'internet-service': 'disable', 'internet-service-id': [], 'internet-service-custom': [], 'rtp-nat': 'disable', 'rtp-addr': [], 'learning-mode': 'disable', 'action': 'accept', 'send-deny-packet': 'disable', 'firewall-session-dirty': 'check-all', 'status': 'enable', 'schedule': 'always', 'schedule-timeout': 'disable', 'service': [{'name': 'ALL', 'q_origin_key': 'ALL'}], 'dscp-match': 'disable', 'dscp-negate': 'disable', 'dscp-value': '000000', 'tcp-session-without-syn': 'disable', 'utm-status': 'disable', 'profile-type': 'single', 'profile-group': '', 'av-profile': '', 'webfilter-profile': '', 'dnsfilter-profile': '', 'spamfilter-profile': '', 'dlp-sensor': '', 'ips-sensor': '', 'application-list': '', 'voip-profile': '', 'icap-profile': '', 'waf-profile': '', 'profile-protocol-options': '', 'ssl-ssh-profile': '', 'logtraffic': 'utm', 'logtraffic-start': 'disable', 'traffic-shaper': '', 'traffic-shaper-reverse': '', 'per-ip-shaper': '', 'application': [], 'app-category': [], 'url-category': [], 'nat': 'enable', 'permit-any-host': 'disable', 'permit-stun-host': 'disable', 'fixedport': 'disable', 'ippool': 'disable', 'poolname': [], 'session-ttl': 0, 'vlan-cos-fwd': 255, 'vlan-cos-rev': 255, 'inbound': 'disable', 'outbound': 'enable', 'natinbound': 'disable', 'natoutbound': 'disable', 'wccp': 'disable', 'ntlm': 'disable', 'ntlm-guest': 'disable', 'ntlm-enabled-browsers': [], 'fsso': 'disable', 'wsso': 'enable', 'rsso': 'disable', 'fsso-agent-for-ntlm': '', 'groups': [], 'users': [], 'devices': [], 'auth-path': 'disable', 'disclaimer': 'disable', 'vpntunnel': '', 'natip': '0.0.0.0 0.0.0.0', 'match-vip': 'disable', 'diffserv-forward': 'disable', 'diffserv-reverse': 'disable', 'diffservcode-forward': '000000', 'diffservcode-rev': '000000', 'tcp-mss-sender': 0, 'tcp-mss-receiver': 0, 'comments': '', 'label': '', 'global-label': '', 'auth-cert': '', 'auth-redirect-addr': '', 'redirect-url': '', 'identity-based-route': '', 'block-notification': 'disable', 'custom-log-fields': [], 'tags': [], 'replacemsg-override-group': '', 'srcaddr-negate': 'disable', 'dstaddr-negate': 'disable', 'service-negate': 'disable', 'internet-service-negate': 'disable', 'timeout-send-rst': 'disable', 'captive-portal-exempt': 'disable', 'ssl-mirror': 'disable', 'ssl-mirror-intf': [], 'scan-botnet-connections': 'disable', 'dsri': 'disable', 'radius-mac-auth-bypass': 'disable', 'delay-tcp-npu-session': 'disable'}]

Update
~~~~~~

To update a firewall policy, you'll need to pass two parameters to the update_firewall_policy function. The ID of
the firewall policy being updated, and a JSON formatted object configuration (only the fields being updated are
required)::

    >>> payload = "{'status': 'disable'}"
    >>> device.update_firewall_policy(500, payload)
    200
    >>> device.get_firewall_policy(500)[0]['status']
    'disable'

Note: you can't just use a python dictionary as your payload. Please refer to the "424" section in
:doc:`common_issues`.

Create
~~~~~~

To create a firewall policy, you'll need to provide two parameters to the create_firewall_policy function. The ID
of the firewall policy being created ("**policy_id**"), and a JSON formatted object configuration ("**data**")::

    >>> payload = {'policyid': 500,
         'name': 'Test Policy',
         'srcintf': [{'name': 'lan'}],
         'dstintf': [{'name': 'wan'}],
         'srcaddr': [{'name': 'all'}],
         'dstaddr': [{'name': 'Test'}],
         'action': 'accept',
         'status': 'enable',
         'schedule': 'always',
         'service': [{'name': 'ALL'}],
         'nat': 'enable',
         'fsso': 'enable',
         'wsso': 'disable',
         'rsso': 'enable'}
    >>> payload = repr(payload)
    >>> device.create_firewall_policy(500, payload)
    200


Move
~~~~

To move a firewall policy, you'll need to call the move_firewall_policy function and pass in three parameters:

    - policy_id (the ID of the policy being moved)
    - position  ("before" or "after")
    - neighbour (the ID of the policy being used as a positional anchor)

.. code-block:: python

    >>> device.move_firewall_policy(policy_id=500,
                                    position="after",
                                    neighbour=2)
    200

Delete
~~~~~~

To delete a firewall policy, you just need to pass the policy ID to the delete_firewall_policy function::

    >>> device.delete_firewall_policy(500)
    200


SNMP Community
--------------

Get
~~~

To get all SNMP communities from your device::

    >>> communities = device.get_snmp_community()

Alternatively, this method looks for a single parameter ("specific") which can be provided to target a single object.
Specific in this instance can be either a community name, or a community ID::

    >>> my_community = device.get_snmp_community('my_community_string')
    >>> my_community = device.get_snmp_community(100)
    >>> device.get_snmp_community('my_community_string') == device.get_snmp_community(100)
    True

The output of this function will be a list. If you've asked for a specific community, this list will be one item long,
but will still be a list.

Each member of the list will be a python dictionary, directly mapped from the FortiGate API's JSON result. This can be
seen in the example below::

    >>> device.get_snmp_community('my_community_string')
    [{'id': 100, 'q_origin_key': 100, 'name': 'my_community_string', 'status': 'enable', 'hosts': [{'id': 1, 'q_origin_key': 1, 'source-ip': '0.0.0.0', 'ip': '192.168.0.0 255.255.255.0', 'ha-direct': 'disable', 'host-type': 'any'}], 'hosts6': [], 'query-v1-status': 'enable', 'query-v1-port': 161, 'query-v2c-status': 'enable', 'query-v2c-port': 161, 'trap-v1-status': 'enable', 'trap-v1-lport': 162, 'trap-v1-rport': 162, 'trap-v2c-status': 'enable', 'trap-v2c-lport': 162, 'trap-v2c-rport': 162, 'events': 'cpu-high mem-low log-full intf-ip vpn-tun-up vpn-tun-down ha-switch ha-hb-failure ips-signature ips-anomaly av-virus av-oversize av-pattern av-fragmented fm-if-change bgp-established bgp-backward-transition ha-member-up ha-member-down ent-conf-change av-conserve av-bypass av-oversize-passed av-oversize-blocked ips-pkg-update ips-fail-open faz-disconnect wc-ap-up wc-ap-down fswctl-session-up fswctl-session-down load-balance-real-server-down'}]


Update
~~~~~~

To update an SNMP Community, you'll need to pass two parameters to the update_snmp_community function. The ID of the
community being updated, and a JSON formatted object configuration (only the fields being updated are required)::

    >>> payload = "{'status': 'disable'}"
    >>> device.update_snmp_community(100, payload)
    200
    >>> device.get_snmp_community(100)[0]['status']
    'disable'

Note: you can't just use a python dictionary as your payload. Please refer to the "424" section in
:doc:`common_issues`.

Create
~~~~~~

To create an SNMP community, you'll need to provide two parameters to the create_snmp_community function. The ID
of the SNMP community being created ("**community_id**"), and a JSON formatted object configuration ("**data**")::

    >>>payload = {'id': 100,
                  'name': 'my_community_string',
                  'status': 'enable',
                  'hosts': [{'ip': '192.168.0.0 255.255.255.0'}]}
    >>> payload = repr(payload)
    >>> device.create_snmp_community(100, payload)


Delete
~~~~~~

To delete an SNMP Community, you just need to pass the community ID to the delete_snmp_community function::

    >>> device.delete_snmp_community(100)
    200