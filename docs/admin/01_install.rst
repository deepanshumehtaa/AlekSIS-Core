Install AlekSIS
===============

From source
-----------

In this section we will install AlekSIS with `uWSGI` and `nGINX` on debian
bullseye.

0. Prerequisites::

 * Debian 11

1. Prepare system

  * Install system dependencies::

    $ apt install uwsgi uwsgi-plugin-python3 nginx-full python3.9 python3.9-dev libldap2-dev libsasl2-dev yarnpkg python3-virtualenv

  * Create and activate virtual environment::

    $ mkdir -p /srv/www/aleksis
    $ mkdir -p /srv/www/aleksis/data/{static,media}
    $ cd /srv/www/aleksis
    $ virtualenv -p python3 --system-site-packages venv
    $ source /srv/www/aleksis/venv/bin/activate
    $ pip install poetry

  * Install and configure PostgreSQL::

    $ apt install postgresql-13
    $ sudo -u postgres createuser -l aleksis -
    $ sudo -u postgres createdb -O aleksis aleksis

  * Configure uWSGI
    .. code-block::
      $ editor /etc/uwsgi/apps-available/aleksis.ini

      [uwsgi]
      vhost = true
      plugins = python3
      master = true
      enable-threads = true
      processes = 20
      wsgi-file = /usr/src/AlekSIS/aleksis/core/wsgi.py
      virtualenv = /srv/www/aleksis/venv
      chdir = /usr/src/AlekSIS
      lazy = true
      lazy-apps = true

      $ ln -s /etc/uwsgi/apps-available/aleksis.ini /etc/uwsgi/apps-enabled/aleksis.ini
      $ service uwsgi restart

  * Configure nGINX::
    .. code-block::
      $ editor /etc/nginx/sites-available/my.aleksis-instance.com
        server {
          listen 80;
          listen [::]:80;

          server_name my.aleksis-instance.com my.aleksis-instance.com;

          return 301 https://$server_name$request_uri;
        }

        server {
                listen 443 ssl http2;
                listen [::]:443 ssl http2;

                ssl_certificate /var/lib/dehydrated/certs/my.aleksis-instance.com/fullchain.pem;
                ssl_certificate_key /var/lib/dehydrated/certs/my.aleksis-instance.com/privkey.pem;
                ssl_trusted_certificate /var/lib/dehydrated/certs/my.aleksis-instance.com/chain.pem;

                server_name my.aleksis-instance.com my.aleksis-instance.com;

                access_log /var/log/nginx/access.log;

                location /static {
                        alias /srv/www/aleksis/data/static;
                }

                location / {
                        uwsgi_pass aleksis;
                        include uwsgi_params;

                        proxy_redirect off;
                        proxy_pass_header Authorization;
                }
        }

      $ ln -s /etc/nginx/sites-available/my.aleksis-instance.com /etc/nginx/sites-enabled/my.aleksis-instance.com
      $ service nginx restart

  * Configure AlekSIS::
    .. code-block::
      $ mkdir /etc/aleksis
      $ editor /etc/aleksis/aleksis.toml
        static = { root = "/srv/www/aleksis/data/static", url = "/static/" }
        media = { root = "/srv/www/aleksis/data/media", url = "/media/" }
        secret_key = "SomeRandomValue"

        [http]
        allowed_hosts = ["my.aleksis-instance.com"]

        [database]
        host = "localhost"
        name = "aleksis"
        username = "aleksis"
        password = "SomeSecretPassword!1"

2. Clone git-Repository and checkout version::

  $ cd /usr/src
  $ git clone https://edugit.org/AlekSIS/official/AlekSIS-Core
  $ cd AlekSIS-Core
  $ git checkout 2.0b

5. Install Dependencies and setup initially::

  $ poetry install
  $ aleksis-admin yarn install
  $ aleksis-admin collectstatic
  $ aleksis-admin migrate

6. Restart uWSGI::

  $ service uwsgi restart

Docker
------

.. _Dynaconf: https://dynaconf.readthedocs.io/en/latest/
