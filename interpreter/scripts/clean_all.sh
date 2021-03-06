#!/bin/bash

echo -e "...Cleaning compiled..."

rm -rf .built
rm -rf .built_logs
rm -rf __pycache__
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

rm -rf db/mongo*
rm -rf dist

echo -e "\n...cleaning ./src/*.js tsc output..."
rm ./src/*.js

echo -e "\n...cleaning .built/ type declarations..."
rm -rf .built/

echo -e "\n...cleaning openssl stuff..."
find demos/ -name "*.key" -print -delete
find demos/ -name "*.pem" -print -delete
find demos/ -name "*.crt" -print -delete
find demos/ -name "*.cert" -print -delete
find demos/ -name "*.csr" -print -delete

find './demos/' -name "leaflet.annotation.j*" -print -delete

find '.' -name "*_render.html" -print -delete
find '.' -name ".DS_*" -print -delete

echo -e "\ncleaning renders..."
find '.' -name "*_render.html" -print -delete

echo -e "\ncleaning bundles..."
find '.' -name "*_bundle.js*" -print -delete

echo -e " ...Done! :) \n"

exit 0
