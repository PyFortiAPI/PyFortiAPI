Getting Started
===============

Create firewall object
----------------------

To start using PyFortiAPI, you'll need to create a firewall object::

    >>> import pyfortiapi
    >>> device = pyfortiapi.FortiGate(ipaddr="",
                                      username="",
                                      password="")


Where IP address should be your FortiGate management IP, and username / password should be obvious.