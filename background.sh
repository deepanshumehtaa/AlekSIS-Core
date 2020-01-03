#!/usr/bin/env bash

cd schoolapps || exit
../env/bin/python manage.py refresh_caches > ../refresh_caches.log
