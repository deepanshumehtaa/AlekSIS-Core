Configuration options
=====================

AlekSIS provides lots of options to configure your instance.

Configuration file
------------------

All settings which are required for running an AlekSIS instance are stored in your configuration file ``/etc/aleksis/aleksis.toml``.

Example configuration file::

    # General config for static, media and secret key, required
    [default]
    static = { root = "/srv/www/aleksis/data/static", url = "/static/" }
    media = { root = "/srv/www/aleksis/data/media", url = "/media/" }
    secret_key = "Xoc8eiwah3neehid2Xi3oomoh4laem"

    # Admin contat, optional
    [default.contact]
    admins = [["AlekSIS - Admins", "root@example.com"]]
    from = 'aleksis@example.com'

    # Allowed hosts, required
    [default.http]
    allowed_hosts = ["localhost"]

    # Database for whole AlekSIS data, required
    [default.database]
    host = "localhost"
    engine = "django.db.backends.postgresql"
    name = "aleksis"
    username = "aleksis"
    password = "aleksis"

    # Maintenance mode and debug, optional
    [default.maintenance]
    statefile = '/var/cache/aleksis/maintenance_mode.txt'
    debug = true

    # Two factor authentication with yubikey enabled, optional
    [default.2fa]
    enabled = true
    yubikey = { enabled = true }

    # Authentication via LDAP, optional
    [default.ldap]
    uri = "ldaps://ldap.myschool.edu"
    bind = { dn = "cn=reader,dc=myschool,dc=edu", password = "secret" }
    map = { first_name = "givenName", last_name = "sn", email = "mail" }

    [default.ldap.users]
    search = { base = "ou=people,dc=myschool,dc=edu", filter = "(uid=%(user)s)" }

    [default.ldap.groups]
    search = { base = "ou=groups,dc=myschool,dc=edu" }
    type = "groupOfNames"
    # Users in group "admins" are superusers
    flags = { is_superuser = "cn=admins,ou=groups,dc=myschool,dc=edu" }

    # Search index, optional
    [default.search]
    backend = "whoosh"
    index = "/srv/www/aleksis/data/whoosh_index"

Configuration in frontend
-------------------------

Everything that must not be configured before the AlekSIS instance fully starts can be configured in frontend, such as site title and logo.

You can find the configuration options in your AlekSIS instance under ``Admin → Configuration``. If you have not installed any additional apps, there the following options:

.. automodule:: aleksis.core.preferences
   :members:
