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

To create an address group, you'll need to provide two parameters to the create_firewall_address function. The name
of the address object being created ("**group_name**"), and a JSON formatted object configuration ("**data**")::

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
    >>> device.get_service_category('Test Category')
    [{'name': 'Test Category', 'q_origin_key': 'Test Category', 'comment': 'Test test test!'}]

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

To delete a service category, you just need to pass the group name to the delete_service_category function::

    >>> device.delete_service_category('Test Category')
    200

Service Groups
--------------

Get
~~~

Update
~~~~~~

Create
~~~~~~

Delete
~~~~~~

Firewall Service
----------------

Get
~~~

Update
~~~~~~

Create
~~~~~~

Delete
~~~~~~

Firewall Policy
---------------

Get
~~~

Update
~~~~~~

Create
~~~~~~

Move
~~~~

Delete
~~~~~~

SNMPv2 Community
----------------

Get
~~~

Create
~~~~~~

Update
~~~~~~

Delete
~~~~~~
