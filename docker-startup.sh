#!/bin/bash

RUN_MODE=${RUN_MODE:-uwsgi}
HTTP_PORT=${HTTP_PORT:-8000}
PREPARE=${PREPARE:-1}

wait_migrations() {
    echo -n "Waiting for migrations to appear"
    while ! aleksis-admin migrate --check >/dev/null 2>&1; do
	sleep 0.5
	echo -n .
    done
    echo
}

wait_database() {
    echo -n "Waiting for database."
    while ! aleksis-admin dbshell -- -c "SELECT 1" >/dev/null 2>&1; do
	sleep 0.5
	echo -n .
    done
    echo
}

prepare_static() {
    aleksis-admin compilescss
    aleksis-admin collectstatic --no-input --clear
}

prepare_database() {
    aleksis-admin migrate
    aleksis-admin createinitialrevisions
}


if [[ -z $ALEKSIS_secret_key ]]; then
    if [[ ! -e /var/lib/aleksis/secret_key ]]; then
	touch /var/lib/aleksis/secret_key; chmod 600 /var/lib/aleksis/secret_key
	LC_ALL=C tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' </dev/urandom | head -c 64 >/var/lib/aleksis/secret_key
    fi
    ALEKSIS_secret_key=$(</var/lib/aleksis/secret_key)
fi

wait_database

case "$RUN_MODE" in
    uwsgi)
	if [[ $PREPARE = 1 ]]; then
	    prepare_database
	    prepare_static
	else
	    wait_migrations
	fi

	exec aleksis-admin runuwsgi -- --http-socket=:$HTTP_PORT
        ;;
    celery-*)
    	if [[ $PREPARE = 1 ]]; then
	    prepare_database
	else
	    wait_migrations
	fi

	exec celery -A aleksis.core ${RUN_MODE#celery-}
	;;
    prepare)
	prepare_database
	prepare_static
	;;
    *)
	exec "$@"
	;;
esac
