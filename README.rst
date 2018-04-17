Foreman API v2 stub server
--------------------------


Prerequisites
=============

.. note::

    Scripts in this folder require Python 3.6+ runtime.

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
