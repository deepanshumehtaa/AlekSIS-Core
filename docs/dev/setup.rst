Setting up the development environment
======================================

BiscuIT and all official apps use `Poetry`_ to manage virtualenvs and
dependencies. You should make yourself a bit confortable with poetry
by reading its documentation.

Poetry makes a lot of stuff very easy, especially managing a virtual
environment that contains BiscuIT and everything you need to run the
framework and selected apps.


Get the source tree
-------------------

To download BiscuIT and all officially bundled apps in their
development version, use Git like so::

  git clone --recurse-submodules https://edugit.org/Teckids/BiscuIT/BiscuIT-ng

If you do not want to download the bundled apps, leave out the
``--recurse-submodules`` option.


Get Poetry
----------

Make sure to have Poetry installed like described in its
documentation. Right now, we encourage using pip to install Poetry
once system-wide (this will change once distributions pick up
Poetry). On Debian, for example, this would be done with::

  sudo apt install python3-pip
  sudo pip3 install poetry

You can use any other of the `Poetry installation methods`_.


Install BiscuIT-ng in its own virtual environment
-------------------------------------------------

Poetry will automatically manage virtual environments per project, so
installing BiscuIT is a matter of::

  poetry install


Running commands in the virtual environment
-------------------------------------------

To run commands in the virtual environment, use Poetry's ``run``
command::

  poetry run ./manage.py runserver

.. _Poetry: https://poetry.eustace.io/
.. _Poetry installation methods: https://poetry.eustace.io/docs/#installation
