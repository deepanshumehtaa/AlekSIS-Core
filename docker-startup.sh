#!/bin/bash

HTTP_PORT=${HTTP_PORT:-8000}
RUN_MODE=uwsgi

if [[ -z $ALEKSIS_secret_key ]]; then
    if [[ ! -e /var/lib/aleksis/secret_key ]]; then
	touch /var/lib/aleksis/secret_key; chmod 600 /var/lib/aleksis/secret_key
	LC_ALL=C tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' </dev/urandom | head -c 64 >/var/lib/aleksis/secret_key
    fi
    ALEKSIS_secret_key=$(</var/lib/aleksis/secret_key)
fi

echo -n "Waiting for database."
while ! aleksis-admin dbshell -- -c "SELECT 1" >/dev/null 2>&1; do
    sleep 0.5
    echo -n .
done
echo

aleksis-admin migrate
aleksis-admin createinitialrevisions
aleksis-admin compilescss
aleksis-admin collectstatic --no-input --clear

case "$RUN_MODE" in
    uwsgi)
	exec aleksis-admin runuwsgi -- --http-socket=:$HTTP_PORT
        ;;
    celery-worker)
	exec celery -A aleksis.core worker
	;;
    celery-beat)
	exec celery -A aleksis.core beat
	;;
    *)
	exec "$@"
	;;
esac
