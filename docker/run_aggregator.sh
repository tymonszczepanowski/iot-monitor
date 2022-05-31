#!/bin/bash

# run aggregator
docker run --rm -itd \
  --network=host \
  --name=pythaggr \
  aggregator 

docker logs pythaggr -f
