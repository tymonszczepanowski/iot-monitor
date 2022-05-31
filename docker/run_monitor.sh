#!/bin/bash

# run monitor 
docker run --rm -it \
  --network=host \
  --name=monitor \
  flask_monitor 
