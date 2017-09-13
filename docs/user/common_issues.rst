Common Issues
=============

424 error when creating or updating objects
-------------------------------------------

424 is the HTTP Status code for "failed dependency". With the FortiGate API, this most frequently appears
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



