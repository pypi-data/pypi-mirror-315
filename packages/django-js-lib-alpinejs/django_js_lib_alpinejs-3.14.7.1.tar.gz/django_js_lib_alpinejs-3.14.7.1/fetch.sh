#!/bin/bash
set -ex

VERSION=$(grep -oP '^__version__\s*=\s*"\K[^"]+' **/__init__.py | cut -d. -f1-3)
echo fetching ${VERSION}...

FOLDER="js_lib_alpinejs/static/js_lib_alpinejs"
curl -sL -o ${FOLDER}/alpine.js "https://unpkg.com/alpinejs@${VERSION}/dist/cdn.js"
curl -sL -o ${FOLDER}/alpine.min.js "https://unpkg.com/alpinejs@${VERSION}/dist/cdn.min.js"

wc -c ${FOLDER}/*
git add -v ${FOLDER}
