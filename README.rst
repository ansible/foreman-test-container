Foreman API v2 stub server
--------------------------


Prerequisites
=============

.. note::

    Scripts in this folder require Python 3.6+ runtime.

Create ``anything.foreman.yaml`` with this contents:

.. code:: yaml

    plugin: foreman
    url: http://localhost:8080
    user: ansible-reader
    password: changeme
    validate_certs: False


Sanitizing
~~~~~~~~~~

.. code:: shell

    $ ./fqdn_sanitizer.py fixtures/*.json


Running
=======

Start the stub:

.. code:: shell

    $ ./flaskapp.py


In docker:

.. code:: shell

    $ make


In docker (dev):

.. code:: shell

    $ make dev


Testing
=======

Run ansible-inventory to test:

.. code:: shell

    $ ansible-inventory -vvvv -i anything.foreman.yaml --list
