Getting Started
===============

Create firewall object
----------------------

To start using PyFortiAPI, you'll need to create a firewall object::

    >>> import pyfortiapi
    >>> device = pyfortiapi.FortiGate(ipaddr="",
                                      username="",
                                      password="")


The parameters shown above are required at a bare minimum:

    - *ipaddr*:     The management IP address of the target device
    - *username*:   The username of the account being used to log in to the device
    - *password*:   The password for previously supplied username

And the following can be provided as optional parameters:

    - *timeout*:    The time in seconds to wait for a response when performing API calls. (**Default: 10**)
    - *vdom*:       The target VDOM within the target device. (**Default: 'root'**)