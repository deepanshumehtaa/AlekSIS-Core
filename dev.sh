#!/bin/sh

set -e

remove_pip_metadata() {
    find . -type d -name pip-wheel-metadata -print0 | xargs -0r rm -rf --
}

case "$1" in
    "install-all")
	cd "$(dirname "$0")"
	remove_pip_metadata
	poetry install
	for d in apps/official/*; do
	    remove_pip_metadata
	    poetry run sh -c "cd $d; poetry install"
	done
	remove_pip_metadata
	poetry run ./manage.py migrate
	poetry run ./manage.py compilemessages
	poetry run ./manage.py collectstatic --no-input
	;;
    "makemessages")
        cd "$(dirname "$0")"
        manage_py=$(realpath manage.py)
        locales="-l ar -l de_DE -l fr -l nb_NO -l tr_TR"
        for d in biscuit/core apps/official/*/biscuit/apps/*; do
        	echo; echo "Entering $d."
        	poetry run sh -c "cd $d; $manage_py makemessages --no-wrap -i static $locales"
        done
        ;;
    *)
	;;
esac
