#!/bin/sh

remove_pip_metadata() {
    find . -type d -name pip-wheel-metadata -print0 | xargs -0r rm -rf --
}

case "$1" in
    "install-all")
        set -e
	cd "$(dirname "$0")"
	remove_pip_metadata
	poetry install
	for d in apps/official/*; do
	    remove_pip_metadata
	    poetry run sh -c "cd $d; poetry install"
	done
	remove_pip_metadata
	poetry run ./manage.py compilemessages
	poetry run ./manage.py yarn install
	poetry run ./manage.py collectstatic --no-input
	set +e
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
    "autopep8")
        cd "$(dirname "$0")"
        for d in biscuit/core apps/official/*/biscuit/apps/*; do
        	echo; echo "Entering $d."
        	poetry run sh -c "cd $d; autopep8 -i -r ."
        done
        ;;
    "pylama")
        cd "$(dirname "$0")"
        tox_ini=$(realpath tox.ini)
        for d in biscuit/core apps/official/*/biscuit/apps/*; do
        	echo; echo "Entering $d."
        	poetry run sh -c "cd $d; pylama -a -o $tox_ini ."
        done
        ;;
    "gource")
        for d in biscuit/core apps/official/*/biscuit/apps/*; do
        	gource --output-custom-log - "$d"
        done | sort -n | gource --log-format custom --background-image biscuit/core/static/img/biscuit-logo.png -
        ;;
    *)
	;;
esac
