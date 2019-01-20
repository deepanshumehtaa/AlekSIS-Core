#!/bin/bash
export BABEL_ENV=production
#./node_modules/.bin/babel src -d dist
#./node_modules/browserify/bin/cmd.js src/App.js -o dist/App.js -t [ babelify --presets [ es2015 react ] ]
webpack --config ./webpack-build.config.js --mode development

cp dist/* ../schoolapps/static/support/
