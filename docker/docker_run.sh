#!/bin/bash

source ../data_aggregator/credentials

# --network=host \

# run mysql database
docker run --rm -d -v mysql:/var/lib/mysql \
  -v mysql_config:/edtc/mysql \
  -p 3306:3306 \
  --name mysqldb \
  -e MYSQL_ROOT_PASSWORD=$PASSWD \
  mysql

# run aggregator
docker run --rm -itd \
  --network=host \
  --name=pythaggr \
  aggregator 

docker logs pythaggr -f
