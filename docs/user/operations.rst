Firewall Address Objects
========================

Get
---

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
------

To update an address object, you'll need to pass two parameters to the update_firewall_address function. The name of
the address object being updated, and a JSON formatted object configuration (only the fields being updated are
required)::

    >>> payload = "{'subnet': '192.168.0.0 255.255.255.0'}"
    >>> device.update_firewall_address('Test', payload)
    200
    >>> device.get_firewall_address('Test')[0]['subnet']
    '192.168.0.0 255.255.255.0'

Note: you can't just use a python dictionary as your payload::

    >>> payload = {'subnet': '10.0.0.0 255.0.0.0'}
    >>> device.update_firewall_address('Test', payload)
    424

However, if you repr the dict to create a string representation of it::

    >>> payload = {'subnet': '10.0.0.0 255.0.0.0'}
    >>> device.update_firewall_address('Test', repr(payload))
    200
    >>> device.get_firewall_address('Test')[0]['subnet']
    '10.0.0.0 255.0.0.0'

Delete
------

To delete an address object, you just need to pass the address name to the delete_firewall_address function::

    >>> device.delete_firewall_address('Test')
    200
    >>> device.get_firewall_address('Test')
    404

Address Groups
==============

Get
---

Update
------

Delete
------

Service Categories
==================

Get
---

Update
------

Delete
------

Service Groups
==============

Get
---

Update
------

Delete
------

Firewall Service
================

Get
---

Update
------

Delete
------

Firewall Policy
===============

Get
---

Update
------

Move
----

Delete
------

SNMPv2 Community
================

Get
---

Update
------

Delete
------
