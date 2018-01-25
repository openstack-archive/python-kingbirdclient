Kingbird
=========

.. image:: https://img.shields.io/pypi/v/python-kingbirdclient.svg
    :target: https://pypi.python.org/pypi/python-kingbirdclient/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/python-kingbirdclient.svg
    :target: https://pypi.python.org/pypi/python-kingbirdclient/
    :alt: Downloads

Centralised service for multi-region OpenStack deployments.

Kingbird is an centralized OpenStack service that provides resource operation and
management across multiple OpenStack instances in a multi-region OpenStack deployment.
This service is part of the OPNFV Multisite project that intends to address
the use cases related to distributed cloud environments.

Kingbird provides features like centralized quota management, centralized view for
distributed virtual resources, global view for tenant level IP/MAC address space management,
synchronisation of ssh keys, images, flavors, etc. across regions.

===============================
python-kingbirdclient
===============================

Python client for Kingbird

This is a client library for Kingbird built on the Kingbird API. It
provides a Python API (the ``kingbirdclient`` module) and a command-line tool
(``kingbird``).

Installation
------------

First of all, clone the repo and go to the repo directory::

    $ git clone https://github.com/openstack/python-kingbirdclient.git
    $ cd python-kingbirdclient

Then just run::

    $ pip install -e .

or::

    $ pip install -r requirements.txt
    $ python setup.py install

Running Kingbird client
-----------------------

If Kingbird authentication is enabled, provide the information about OpenStack
auth to environment variables. Type::

    $ export OS_PROJECT_DOMAIN_ID=<PROJECT_DOMAIN_ID>
    $ export OS_REGION_NAME=<Region>
    $ export OS_USER_DOMAIN_ID=<USER_DOMAIN_ID>
    $ export OS_PROJECT_NAME=<project_name>
    $ export OS_IDENTITY_API_VERSION=<identity_version>
    $ export OS_PASSWORD=<password>
    $ export OS_AUTH_TYPE=<auth_type>
    $ export OS_AUTH_URL=http://<Keystone_host>/identity
    $ export OS_USERNAME=<user_name>
    $ export OS_TENANT_NAME=<tenant_name>

.. note:: In client, we use Keystone auth version v3 as
          server supports only v3.*

To make sure Kingbird client works, type::

    $ kingbird quota defaults

or::

    $ kingbird sync list


You can see the list of available commands typing::

    $ kingbird --help

About sync template command
============================
Provide the input file in .yaml/.yml/.json to sync multiple resource-types to multiple regions
Sample input file for .yaml/.yml
--------------------------------
Eg::

    Sync:
    - resource_type: fake_resource_type
      resources:
      - fake_resource_1
      - fake_resource_2
      source:
      - fake_source_region
      target:
      - fake_target_region_1
      - fake_target_region_2
      force: "True"


Sample input file for .json
--------------------------
Eg::

    {
      "Sync": [
        {
          "resource_type": "fake_resource_type",
          "resources": [
            "fake_resource_1",
            "fake_resource_2"
          ],
          "source":["fake_source_region"],
          "target":["fake_target_region_1","fake_target_region_2"],
          "force":"True"
        }
      ]
    }

Note: "force" is optional in .yaml and .json files.

Useful Links
============
* Free software: Apache license
* `PyPi`_ - package installation
* `Launchpad project`_ - release management
* `Blueprints`_ - feature specifications
* `Bugs` - issue tracking
* `Source`_
* `How to Contribute`_
* `Documentation`_

.. _PyPi: https://pypi.python.org/pypi/python-kingbirdclient
.. _Launchpad project: https://launchpad.net/python-kingbirdclient
.. _Bugs: https://bugs.launchpad.net/python-kingbirdclient
.. _Blueprints: https://blueprints.launchpad.net/python-kingbirdclient
.. _Source: http://git.openstack.org/cgit/openstack/python-kingbirdclient
.. _How to Contribute: http://docs.openstack.org/infra/manual/developers.html
.. _Documentation: http://docs.openstack.org/developer/python-kingbirdclient
