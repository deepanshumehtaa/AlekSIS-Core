Installing BiscuIT with PostgreSQL backend
=========================================

PostgreSQL is the preferred database backend for BiscuIT. You should use it
in every production setup and use SQLite only for testing.


Install the PostgreSQL server
-----------------------------

On Debian, install the postgresql server package with::

  sudo apt install postgresql


Create a database and user
--------------------------

On Debian, you can use the following commands to create the database and a
user who owns it::

  sudo -u postgres createuser -D -P -R -S biscuit
  sudo -u postgres createdb -E UTF-8 -O biscuit -T template0 -l C.UTF-8 biscuit

When asked for the database user password, choose a secure, preferrably
random, password. You can generate one using the pwgen utility if you like::

  pwgen 16 1


Configure BiscuIT to use PostgreSQL
-----------------------------------

Fill in the configuration under `/etc/biscuit/*.toml`::

  [default.database]
  engine = "django.db.backends.postgresql"
  name = "biscuit"
  username = "biscuit"
  password = "Y0urV3ryR4nd0mP4ssw0rd"

Don't forget to run the migrations, like described in the basic setup guide.
