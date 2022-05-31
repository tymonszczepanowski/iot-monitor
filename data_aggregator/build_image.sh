#!/bin/bash
docker rmi aggregator
docker build . -t aggregator
