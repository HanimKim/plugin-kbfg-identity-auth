#! /bin/bash
# Build a docker image
cd ..
docker build -t pyengine/plugin-kbfg-sso .
docker tag pyengine/keycloak pyengine/plugin-kbfg-sso:1.0
docker tag pyengine/keycloak spaceone/plugin-kbfg-sso:1.0
