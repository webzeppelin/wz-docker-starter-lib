#!/bin/bash

cd /opt/dex

# load the env
source ./env.sh

# start the overlord
# ./bin/dex-overlord &
# echo "Waiting for overlord to start..."
# until $(curl --output /dev/null --silent --fail http://localhost:5557/health); do
#     printf '.'
#     sleep 1
# done

./bin/dex-worker
