#!/bin/bash

source ../data_aggregator/credentials
# run mysql database
docker run --rm -d -v mysql:/var/lib/mysql \
  -v mysql_config:/edtc/mysql \
  --name mysqldb \
  --network=host \
  -e MYSQL_ROOT_PASSWORD=$PASSWD \
  mysql
