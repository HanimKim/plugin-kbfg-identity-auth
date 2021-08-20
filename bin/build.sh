#! /bin/bash
# Build a docker image
DEFAULT=0.1
VER=${1:-$DEFAULT}
cd ..
docker build -t pyengine/plugin-kbfg-identity-auth .
docker tag pyengine/plugin-kbfg-identity-auth pyengine/plugin-kbfg-identity-auth:${VER}
