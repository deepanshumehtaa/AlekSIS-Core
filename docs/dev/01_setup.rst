Setting up the development environment
======================================

BiscuIT and all official apps use `Poetry`_ to manage virtualenvs and
dependencies. You should make yourself a bit confortable with poetry
by reading its documentation.

Poetry makes a lot of stuff very easy, especially managing a virtual
environment that contains BiscuIT and everything you need to run the
framework and selected apps.

Also, `Yarn`_ is needed to resolve JavaScript dependencies.

Get the source tree
-------------------

To download BiscuIT and all officially bundled apps in their
development version, use Git like so::

  git clone --recurse-submodules https://edugit.org/BiscuIT/BiscuIT-ng

If you do not want to download the bundled apps, leave out the
``--recurse-submodules`` option.


Install native dependencies
---------------------------

Some system libraries are required to install BiscuIT::

  sudo apt install libpq5 libpq-dev libssl-dev python3-dev yarnpkg python3-pip python3-venv


Get Poetry
----------

Make sure to have Poetry installed like described in its
documentation. Right now, we encourage using pip to install Poetry
once system-wide (this will change once distributions pick up
Poetry). On Debian, for example, this would be done with::

  sudo pip3 install poetry

You can use any other of the `Poetry installation methods`_.


Install BiscuIT-ng in its own virtual environment
-------------------------------------------------

Poetry will automatically manage virtual environments per project, so
installing BiscuIT is a matter of::

  poetry install


Regular tasks
-------------

After making changes to the environment, e.g. installing apps or updates,
some maintenance tasks need to be done:

1. Download and install JavaScript dependencies
2. Collect static files
3. Run database migrations

All three steps can be done with the ``poetry run`` command and
``manage.py``::

  poetry run ./manage.py yarn install
  poetry run ./manage.py collectstatic
  poetry run ./manage.py compilemessages
  poetry run ./manage.py migrate

(You might need database settings for the `migrate` command; see below.)

Running the development server
------------------------------

The development server can be started using Django's ``runserver`` command.
You can either configure BiscuIT like in a production environment, or pass
basic settings in as environment variable. Here is an example that runs the
development server against a local PostgreSQL database with password
`biscuit` (all else remains default) and with the `debug` setting enabled::

  BISCUIT_debug=true BISCUIT_database__password=biscuit poetry run ./manage.py runserver

.. figure:: /screenshots/index.png
   :scale: 50%
   :alt: Screenshot of index page

   After installing the development environment with default settings,
   you should see the index page with the Bootstrap style.

.. _Poetry: https://poetry.eustace.io/
.. _Poetry installation methods: https://poetry.eustace.io/docs/#installation
.. _Yarn: https://yarnpkg.com
