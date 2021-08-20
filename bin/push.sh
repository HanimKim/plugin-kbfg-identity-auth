#!/usr/bin/env bash
# How to upload
DEFAULT=0.1
VER=${1:-$DEFAULT}
./build.sh ${VER}
docker push pyengine/plugin-kbfg-identity-auth:${VER}
#docker push spaceone/plugin-kbfg-sso:1.0
