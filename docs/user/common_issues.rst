Common Issues
=============

424 error when creating / updating objects
------------------------------------------

424 is the HTTP Status code for "Failed Dependency". With the FortiGate API, this most frequently appears
if required parameters are missing, or if parameters are incorrectly handled.

When creating or updating an object via PyFortiAPI, you need to provide a JSON formatted string of parameters. While
it may look like the examples provided in the user guide are python dictionaries, they're not *exactly*. All of the
parameter payloads used in the examples provided are JSON formatted string representations of python dictionaries.

Take for example, what happens when we fire a straight dictionary of values to the device::

    >>> payload = {'subnet': '10.0.0.0 255.0.0.0'}
    >>> device.update_firewall_address('Test', payload)
    424

However, if you repr the dictionary to create a string representation::

    >>> payload = {'subnet': '10.0.0.0 255.0.0.0'}
    >>> device.update_firewall_address('Test', repr(payload))
    200
    >>> device.get_firewall_address('Test')[0]['subnet']
    '10.0.0.0 255.0.0.0'

500 error when creating / updating / deleting objects
-----------------------------------------------------

As you probably know, 500 is the HTTP Status Code for "Internal Server Error".

When dealing with the FortiGate API, the most common causes are incorrect parameter names or malformed parameters when
trying to create / update, or existing references to that object when trying to delete.

Double check your parameter names are correct. If in doubt, **GET** an existing object and check out the syntax.
If you're deleting an object and don't know where it's being referenced, it's probably a good idea to track down and
evaluate those references.