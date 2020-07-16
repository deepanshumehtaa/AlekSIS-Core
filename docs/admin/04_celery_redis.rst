Asyncronous tasks with Celery
=============================

Celery is able to run asyncronous tasks provided by AlekSIS, e.g. sending of notifications or backing up AlekSIS database and media.

Celery and Celery beat worker
-----------------------------

To run asyncronous Celery tasks, you will need a running Celery and Celery beat worker on your system. You can find instructions to run them via systemd in the `Celery docs`_

Enable celery in AlekSIS configuration
--------------------------------------

To enable Celery in your AlekSIS instance, add the following to your ``/etc/aleksis/aleksis.toml``::

    [default.celery]
    enabled = true

Celery with redis
=================

Redis is a key-value database very similar to memecache. Redis provides natvie support for atomically querying and manipulating lists and sets.

Install redis server
--------------------

On Debian you just have to intall the ``redis-server`` package::

    sudo apt install redis-server

After you've installed the redis server, you should start it. If you're using systemd you can do this like this::

    sudo service redis-server start

For other operating systems please look into their package index.

Enable redis in AlekSIS configuration
-------------------------------------

To enable the Celery broker in your AlekSIS instance, add the following to your ``/etc/aleksis/aleksis.toml``::

    [default.celery]
    enabled = true
    broker = true

.. _Celery docs: https://docs.celeryproject.org/en/stable/userguide/daemonizing.html
