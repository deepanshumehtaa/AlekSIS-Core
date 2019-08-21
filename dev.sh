#!/bin/sh

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
	;;
    *)
	;;
esac
