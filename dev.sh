#!/usr/bin/env mksh

remove_pip_metadata() {
    find . -type d -name pip-wheel-metadata -print0 | xargs -0r rm -rf --
}

case "$1" in
    "install-all")
	set -e
	cd "$(dirname "$0")"
	remove_pip_metadata
	poetry lock
	poetry install
	for d in apps/official/*; do
	    remove_pip_metadata
	    poetry run sh -c "cd $d; poetry lock; poetry install"
	done
	remove_pip_metadata
	poetry run ./manage.py compilemessages
	poetry run ./manage.py yarn install
	poetry run ./manage.py collectstatic --no-input
	set +e
	exit
	;;
    "makemessages")
	cd "$(dirname "$0")"
	manage_py=$(realpath manage.py)
	locales="-l ar -l de_DE -l fr -l nb_NO -l tr_TR -l la"
	for d in aleksis/core apps/official/*/aleksis/apps/*; do
		echo; echo "Entering $d."
		poetry run sh -c "cd $d; $manage_py makemessages --no-wrap -e html,txt,py,email -i static $locales"
		poetry run sh -c "cd $d; $manage_py makemessages --no-wrap -d djangojs $locales"
	done
	exit
	;;
    "autopep8")
	cd "$(dirname "$0")"
	for d in aleksis/core apps/official/*/aleksis/apps/*; do
		echo; echo "Entering $d."
		poetry run sh -c "cd $d; autopep8 -i -r ."
	done
	exit
	;;
    "pylama")
	cd "$(dirname "$0")"
	tox_ini=$(realpath tox.ini)
	for d in aleksis/core apps/official/*/aleksis/apps/*; do
		echo; echo "Entering $d."
		poetry run sh -c "cd $d; pylama -a -o $tox_ini ."
	done
	exit
	;;
    "gource")
	for d in . apps/official/*; do
		gource --output-custom-log - "$d"
	done | sort -n | gource --log-format custom --background-image aleksis/core/static/img/aleksis-icon.png "$@" -
	exit
	;;

    "devstats-commits")
	# Copyright © 2018
	#	mirabilos <m@mirbsd.org>
	# Copyright © 2017
	#	mirabilos <t.glaser@tarent.de>
	# Copyright © 2015, 2017, 2020
	#	mirabilos <thorsten.glaser@teckids.org>
	#
	# Provided that these terms and disclaimer and all copyright notices
	# are retained or reproduced in an accompanying document, permission
	# is granted to deal in this work without restriction, including un‐
	# limited rights to use, publicly perform, distribute, sell, modify,
	# merge, give away, or sublicence.
	#
	# This work is provided “AS IS” and WITHOUT WARRANTY of any kind, to
	# the utmost extent permitted by applicable law, neither express nor
	# implied; without malicious intent or gross negligence. In no event
	# may a licensor, author or contributor be held liable for indirect,
	# direct, other damage, loss, or other issues arising in any way out
	# of dealing in the work, even if advised of the possibility of such
	# damage or existence of a defect, except proven that it results out
	# of said person’s immediate fault when using the work as intended.

	set -e
	set -o pipefail
	unset LANGUAGE
	export LC_ALL=C.UTF-8
	set -o utf8-mode

	for d in . apps/official/*; do
		cd "$d"
		if [[ ! -s pyproject.toml ]]; then
			print -ru2 "E: missing pyproject.toml in ${d@Q}"
			print -ru2 "N: maybe you forgot the submodules?"
			print -ru2 "N: try git submodule update --init --recursive"
			exit 1
		fi
		cd "$OLDPWD"
	done
	for d in . apps/official/*; do
		cd "$d"
		git log --pretty=tformat:%aN
		cd "$OLDPWD"
	done | sort | uniq -c | sort -nr |&
	maxnum=0
	maxlen=0
	set -A nums
	set -A names
	nlines=0
	while IFS= read -pr line; do
		line=${line##*( )}
		num=${line%% *}
		line=${line##+([0-9]) }
		#print -r -- "<$num><$line>"
		(( maxnum = num > maxnum ? num : maxnum ))
		len=${%line}
		if (( len == -1 )); then
			len=${#line}
			print -ru2 -- "W: assuming length $len for author ${line@Q}"
		fi
		(( maxlen = len > maxlen ? len : maxlen ))
		nums[nlines]=$num
		names[nlines++]=$line
	done
	w=$COLUMNS
	if (( (w -= 1 + maxlen + 1) < 1 )); then
		print -ru2 -- "E: terminal too small, need $((-w+1)) more columns"
		exit 1
	fi
	if (( maxnum < 1 )); then
		print -ru2 -- "E: no commits"
		exit 1
	fi
	set +e
	typeset -R$maxlen pname
	mbar=██
	nlen=0
	num=$maxnum
	while ((# num > 0 )); do
		mbar+=█
		((# ++nlen ))
		((# num /= 10 ))
	done
	typeset -R$nlen pnum
	print '\e[0m'
	line=-1
	while (( ++line < nlines )); do
		bar=
		((# num = (nums[line] * w * 8) / maxnum ))
		while ((# num >= 8 )); do
			bar+=█
			((# num -= 8 ))
		done
		case $num {
		(7) bar+=▉ ;;
		(6) bar+=▊ ;;
		(5) bar+=▋ ;;
		(4) bar+=▌ ;;
		(3) bar+=▍ ;;
		(2) bar+=▎ ;;
		(1) bar+=▏ ;;
		}
		pname=${names[line]}
		if [[ $bar = "$mbar"* ]]; then
			pnum=${nums[line]}
			bar=$'\e[7m '$pnum$' \e[0m'${bar#"$mbar"}
		else
			bar+=" ${nums[line]}"
		fi
		print -r -- "$pname $bar"
	done
	exit
	;;
    *)
	print -ru2 -- "E: unknown command ${1@Q}"
	exit 1
	;;
esac
