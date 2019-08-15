Installing apps into development environment
============================================

Officially bundled apps
-----------------------

Officially bundlede apps are available in the ``apps/official/``
sub-folder as Git submodules. If you followed the documentation, they
will already be checked out in the version required for the bundle you
are running.

Installing apps into the existing virtual environment is a bit awkward::

  poetry run sh -c "cd apps/official/BiscuIT-App-Exlibris; poetry install"

This will install the Exlibris app (library management) app by using a
shell for first ``cd``'ing into the app directory and then using
poetry to install the app.


Migrate the database
--------------------

After installing or updating any apps, the database must be updated as
well by running Django's ``migrate`` command::

  poetry run ./manage.py migrate
