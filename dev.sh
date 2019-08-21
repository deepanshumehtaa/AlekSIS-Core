#!/bin/sh

case "$1" in
    "install-all")
	cd "$(dirname "$0")"
	poetry install
	for d in apps/official/*; do
	    poetry run sh -c "cd $d; poetry install"
	done
	poetry run ./manage.py migrate
	;;
    *)
	;;
esac
