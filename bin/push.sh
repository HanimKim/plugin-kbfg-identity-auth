#!/usr/bin/env bash
# How to upload
./build.sh
docker push pyengine/plugin-kbfg-sso:1.0
docker push spaceone/plugin-kbfg-sso:1.0
