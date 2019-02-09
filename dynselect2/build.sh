#!/usr/bin/env bash
cp ../dynselect/src/App.js src/App.js
read -p "Now remove CSS line. Then press [ENTER]."
cat mounter.js >> src/App.js
gulp build
cp build/* ../schoolapps/static/support/
rm build/*
