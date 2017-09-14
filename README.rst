PyFortiAPI
==========

.. image:: https://img.shields.io/github/license/jsimpso/PyFortiAPI.svg   
    :target: https://github.com/jsimpso/PyFortiAPI 
    
.. image:: https://img.shields.io/pypi/v/pyfortiapi.svg
    :target: https://pypi.python.org/pypi/PyFortiAPI

.. image:: https://img.shields.io/pypi/pyversions/pyfortiapi.svg   
    :target: https://pypi.python.org/pypi/PyFortiAPI
  
    
A Python wrapper for the FortiGate REST API (FortiOS 5.4.x+)

Here's a quick usage example:

.. code-block:: python

  >>> import pyfortiapi
  >>> 
  >>> device = pyfortiapi.FortiGate(ipaddr="192.168.0.99", username="admin", password="Guest")
  >>> device.get_firewall_address('Test')
  404
  >>> create_payload = "{'name': 'Test', 'type': 'subnet', 'subnet': '192.168.0.0 255.255.255.0'}"
  >>> device.create_firewall_address('Test', create_payload)
  200
  >>> device.get_firewall_address('Test')
  [{'name': 'Test', 'q_origin_key': 'Test', 'uuid': '9bf2e12a-977b-51e7-ff8d-22d7cf593ab9', 'subnet': '192.168.0.0 255.255.255.0', 'type': 'ipmask', 'start-ip': '192.168.0.0', 'end-ip': '255.255.0.0', 'fqdn': '', 'country': '\n\x05', 'wildcard-fqdn': '', 'cache-ttl': 0, 'wildcard': '192.168.0.0 255.255.0.0', 'comment': '', 'visibility': 'enable', 'associated-interface': '', 'color': 0, 'tags': [], 'allow-routing': 'disable'}]
  >>> update_payload = "{'subnet': '10.0.0.0 255.0.0.0'}"
  >>> device.update_firewall_address('Test', update_payload)
  200
  >>> device.get_firewall_address('Test')
  [{'name': 'Test', 'q_origin_key': 'Test', 'uuid': '9bf2e12a-977b-51e7-ff8d-22d7cf593ab9', 'subnet': '10.0.0.0 255.0.0.0', 'type': 'ipmask', 'start-ip': '10.0.0.0', 'end-ip': '255.0.0.0', 'fqdn': '', 'country': '\n', 'wildcard-fqdn': '', 'cache-ttl': 0, 'wildcard': '10.0.0.0 255.0.0.0', 'comment': '', 'visibility': 'enable', 'associated-interface': '', 'color': 0, 'tags': [], 'allow-routing': 'disable'}]
  >>> device.delete_firewall_address('Test')
  200
  >>> device.get_firewall_address('Test')
  404


Installation
------------

To install, just:

.. code-block:: none

  pip install pyfortiapi
  
Documentation
-------------

Extended documentation is available at https://pyfortiapi.readthedocs.io


