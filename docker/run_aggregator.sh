#!/bin/bash

# run aggregator
docker run --rm -itd \
  -v /etc/localtime:/etc/localtime:ro \
  --network=host \
  --name=pythaggr \
  aggregator 

docker logs pythaggr -f
