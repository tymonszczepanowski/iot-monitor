#!/bin/bash
docker rmi flask_monitor
docker build . -t flask_monitor 
