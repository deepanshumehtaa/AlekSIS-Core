Install AlekSIS
===============

From source
-----------

In this section we will install AlekSIS with `uWSGI` and `nGINX` on debian
bullseye.

1. Prerequisites::

 * Debian 11

1. Prepare system

  * Install system dependencies::

    $ apt install uwsgi uwsgi-plugin-python3 nginx-full python3.9 python3.9-dev libldap2-dev libsasl2-dev yarnpkg python3-virtualenv chromium redis-server

  * Create and activate virtual environment::

    $ mkdir -p /srv/www/aleksis
    $ mkdir -p /srv/www/aleksis/data/{static,media}
    $ cd /srv/www/aleksis
    $ python3 -m venv
    $ source /srv/www/aleksis/venv/bin/activate
    $ pip install poetry

  * Install and configure PostgreSQL::

    $ apt install postgresql-13
    $ sudo -u postgres createuser -l aleksis -
    $ sudo -u postgres createdb -O aleksis aleksis

  * Configure uWSGI::

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

  * Get SSL ssl certificate
    * https://certbot.eff.org/instructions
  * Configure nGINX::
      $ editor /etc/nginx/sites-available/aleksis.example.com
        server {
          listen 80;
          listen [::]:80;

          server_name aleksis.example.com;

          return 301 https://$server_name$request_uri;
        }

        server {
                listen 443 ssl http2;
                listen [::]:443 ssl http2;

                ssl_certificate /etc/letsencrypt/certs/aleksis.example.com/fullchain.pem;
                ssl_certificate_key /etc/letsencrypt/certs/aleksis.example.com/privkey.pem;
                ssl_trusted_certificate /etc/letsencrypt/certs/aleksis.example.com/chain.pem;

                server_name aleksis.example.com;

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

      $ ln -s /etc/nginx/sites-available/aleksis.example.com /etc/nginx/sites-enabled/aleksis.example.com
      $ service nginx restart

  * Configure AlekSIS::
      $ mkdir /etc/aleksis
      $ editor /etc/aleksis/aleksis.toml
        static = { root = "/srv/www/aleksis/data/static", url = "/static/" }
        media = { root = "/srv/www/aleksis/data/media", url = "/media/" }
        secret_key = "SomeRandomValue"

        [http]
        allowed_hosts = ["aleksis.example.com"]

        [database]
        host = "localhost"
        name = "aleksis"
        username = "aleksis"
        password = "SomeSecretPassword!1"

1. Clone git repository and checkout version::

  $ cd /usr/src
  $ git clone https://edugit.org/AlekSIS/official/AlekSIS-Core
  $ cd AlekSIS-Core
  $ git checkout 2.0b

1. Install dependencies and setup initially::

  $ poetry install
  $ aleksis-admin yarn install
  $ aleksis-admin collectstatic
  $ aleksis-admin migrate

1. Restart uWSGI::

  $ service uwsgi restart

Docker with `docker-compose`
---------------------------

1. Prerequisites::

 * System with docker and docker-compose installed

1. Run docker image::

    $ git clone https://edugit.org/AlekSIS/Official/AlekSIS
    $ docker-compose up -d

.. _Dynaconf: https://dynaconf.readthedocs.io/en/latest/
